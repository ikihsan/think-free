"""Identifier allocation must read the shared base, not this working tree.

Twelve collisions in two days came from one line: `tasks.next_task_id` listed
this VM's `tasks/` directory to pick the next number, so a VM that had not
fetched handed out a number another VM had already published. The bytes are in
history - `83aa9a4` and `569a7ce` each added a different `tasks/T-0024-*.md` -
and the repair each time was a renumbering commit.

Every fleet test here builds a real bare remote and real clones, because the
property under test is what git records at the shared base, not what this
process happens to have cached. T-0030 builds the other half of the fix, the
gate that refuses a commit defining one identifier twice; the ceiling of the
half here is stated in `STATE-defects.md`.
"""

from __future__ import annotations

from harness import RepoTest, git, make_fleet

from originlib import idalloc, taskops, tasks


class FleetBase(RepoTest):
    """A bare remote, two clones, and one task already published."""

    def setUp(self) -> None:
        super().setUp()
        self.fleet = make_fleet(self)
        self.seed = self.fleet / "seed"
        self.vm_a = self.fleet / "vm-a"
        self.vm_b = self.fleet / "vm-b"
        self.use(self.seed)
        taskops.create("published task", "true")
        self.publish(self.seed, "add task")
        for clone in (self.vm_a, self.vm_b):
            git(clone, "pull", "-q", "--ff-only")

    def publish(self, clone, message: str = "work") -> None:
        git(clone, "add", "-A")
        git(clone, "commit", "-qm", message)
        git(clone, "push", "-q", "origin", "research/origin")

    def write_on(self, clone, relative: str, content: str) -> None:
        path = clone / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")

    def local_ids(self, clone) -> list[str]:
        self.use(clone)
        return [task.path.name for task in tasks.all_tasks()]


class StaleTreeTaskAllocationTest(FleetBase):
    """The defect itself: a tree behind the base must not allocate from itself."""

    def test_a_stale_tree_does_not_take_a_number_the_base_defines(self) -> None:
        self.use(self.vm_a)
        published = taskops.create("created on vm-a", "true")
        self.assertEqual(published.task_id, "T-0002")
        self.publish(self.vm_a, "add vm-a task")
        # vm-b's working tree still holds only T-0001: it has not fetched.
        self.use(self.vm_b)
        self.assertEqual([task.task_id for task in tasks.all_tasks()], ["T-0001"])
        self.assertEqual(taskops.create("created on vm-b", "true").task_id, "T-0003")

    def test_allocation_fetches_the_base_without_touching_the_working_tree(self) -> None:
        self.use(self.vm_a)
        self.publish_after_task("vm-a task")
        self.use(self.vm_b)
        self.assertEqual(idalloc.next_identifier("T"), "T-0003")
        # The tree is still stale - that is the condition under test - while the
        # remote-tracking ref has moved.
        self.assertEqual([task.task_id for task in tasks.all_tasks()], ["T-0001"])
        base = git(self.vm_b, "rev-parse", "origin/research/origin")
        self.assertIn("T-0002-", " ".join(git(self.vm_b, "ls-tree", "--name-only", base, "tasks/").split()))

    def publish_after_task(self, goal: str) -> str:
        task = taskops.create(goal, "true")
        self.publish(self.vm_a, f"add {goal}")
        return task.task_id


class ProvenanceTest(FleetBase):
    """A number must say which record it was read from."""

    def test_the_source_names_the_ref_and_the_commit(self) -> None:
        allocation = idalloc.allocate("T")
        self.assertTrue(allocation.remote_read)
        self.assertIn("origin/research/origin", allocation.source())
        self.assertEqual(len(allocation.remote_sha), 40)
        self.assertIn(allocation.remote_sha[:7], allocation.source())

    def test_an_unreachable_base_is_reported_rather_than_hidden(self) -> None:
        git(self.vm_b, "remote", "set-url", "origin", "/nonexistent-shared-base.git")
        self.use(self.vm_b)
        allocation = idalloc.allocate("T")
        # The last fetched snapshot is still readable, and still the best
        # evidence available; what must not happen is reporting it as current.
        self.assertTrue(allocation.remote_read)
        self.assertFalse(allocation.fetched)
        self.assertTrue(allocation.unreachable)
        self.assertIn("fetch failed", allocation.source())
        self.assertEqual(allocation.next_id, "T-0002")


class NoRemoteTest(RepoTest):
    def test_no_remote_means_the_working_tree_and_says_so(self) -> None:
        allocation = idalloc.allocate("T")
        self.assertFalse(allocation.remote_ref)
        self.assertIn("no shared base", allocation.source())
        self.assertEqual(allocation.next_id, "T-0001")


class WithdrawnNumberTest(RepoTest):
    """A number that was published once is not handed out again."""

    def test_a_deleted_task_file_does_not_recycle_its_number(self) -> None:
        created = taskops.create("withdrawn", "true")
        created.path.unlink()
        self.assertEqual(tasks.next_task_id(), "T-0002")


class FindingsAndDecisionTest(RepoTest):
    """F and D numbers are read the same way, which is the point of the command."""

    def test_definitions_and_index_rows_both_count(self) -> None:
        self.write("FAILURES.md", "| Id | Subject |\n|---|---|\n| F001 | one |\n| F002 | two |\n")
        self.write("FAILURES-findings.md", "## F003 — three\n")
        self.assertEqual(idalloc.next_identifier("F"), "F004")

    def test_a_prose_mention_is_not_an_allocation(self) -> None:
        self.write(
            "FAILURES-findings.md",
            "## F003 — three\n\nThe earlier one, F010, was a different subject.\n",
        )
        self.assertEqual(idalloc.next_identifier("F"), "F004")

    def test_an_identifier_inside_a_quoted_string_is_not_an_allocation(self) -> None:
        """F097's own row quotes the bike serial SNACEOSF18391.

        The cell pattern has no word boundary, so that serial reads as finding
        183 and the allocator hands out F184. The boundary is what keeps a
        quoted string from allocating an identifier (defect 26).
        """
        self.write(
            "FAILURES.md",
            "| Id | Subject |\n|---|---|\n"
            "| F097 | Bike serial `SNACEOSF18391` decoded by no source. |\n",
        )
        self.assertEqual(idalloc.next_identifier("F"), "F098")

    def test_the_boundary_holds_from_the_trailing_side_too(self) -> None:
        self.write(
            "FAILURES.md",
            "| Id | Subject |\n|---|---|\n| F004 | the tag SNACEOSF1839A is one row |\n",
        )
        self.assertEqual(idalloc.next_identifier("F"), "F005")

    def test_decision_spans_declare_both_endpoints(self) -> None:
        self.write("DECISIONS.md", "| File | Decisions |\n|---|---|\n| DECISIONS-GATING.md | D024–D029 |\n")
        self.assertEqual(idalloc.next_identifier("D"), "D030")

    def test_an_unknown_kind_is_refused_by_name(self) -> None:
        with self.assertRaises(idalloc.AllocationError) as caught:
            idalloc.allocate("Q")
        self.assertIn("T, F, D", str(caught.exception))


class CommandTest(RepoTest):
    """The CLI contract, including the exit code for a misuse."""

    def test_id_next_prints_the_number_and_its_source(self) -> None:
        self.assertEqual(self.cli("id", "next", "T"), 0)
        self.assertIn("T-0001", self.output())
        self.assertIn("working tree", self.output())

    def test_id_next_refuses_a_kind_it_does_not_know_without_a_traceback(self) -> None:
        self.assertEqual(self.cli("id", "next", "Q"), 1)
        self.assertNotIn("Traceback", self.errors())

    def test_task_new_reports_where_its_number_came_from(self) -> None:
        self.assertEqual(self.cli("task", "new", "--goal", "reported", "--verify", "true"), 0)
        self.assertIn("T-0001", self.output())
        self.assertIn("working tree", self.output())


class FleetCommandTest(FleetBase):
    def test_task_new_names_the_shared_base_it_allocated_from(self) -> None:
        self.use(self.vm_b)
        self.assertEqual(self.cli("task", "new", "--goal", "on vm-b", "--verify", "true"), 0)
        self.assertIn("origin/research/origin", self.output())

    def test_id_next_reads_the_base_for_findings_too(self) -> None:
        self.write_on(self.vm_a, "FAILURES-findings.md", "## F018 — eighteen\n")
        self.publish(self.vm_a, "add a finding")
        self.use(self.vm_b)
        self.assertEqual(self.cli("id", "next", "F"), 0)
        self.assertIn("F019", self.output())