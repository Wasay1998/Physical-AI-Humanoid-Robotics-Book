# Tasks: Create AI Textbook

**Input**: Design documents from `/specs/001-create-ai-textbook/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: Testing for this feature will be manual, based on the acceptance criteria in `spec.md`.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- All paths are relative to the repository root.

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic Docusaurus setup.

- [x] T001 Initialize Docusaurus project in a new directory `ai-book` using `npx create-docusaurus@latest ai-book classic`
- [x] T002 Update `ai-book/docusaurus.config.js` with the project title "Physical AI & Humanoid Robotics" and basic metadata.
- [x] T003 Delete the default `ai-book/docs` directory content.
- [x] T004 Delete the `ai-book/blog` directory.
- [x] T005 Create the main docs landing page at `ai-book/docs/index.md`.

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented.

**⚠️ CRITICAL**: No user story work can begin until this phase is complete.

- [x] T006 Create the sidebar definition file at `ai-book/sidebars.js`.

**Checkpoint**: Foundation ready - user story implementation can now begin.

---

## Phase 3: User Story 1 - Browse and Read Textbook Content (Priority: P1) 🎯 MVP

**Goal**: As a learner, I want to navigate the textbook structure through a sidebar and read the content of each lesson, so that I can learn about Physical AI and Humanoid Robotics.

**Independent Test**: The generated Docusaurus site can be launched (`npm run start`), the sidebar shows the full module/chapter/lesson structure, and clicking a link displays the corresponding placeholder page.

### Implementation for User Story 1

- [x] T007 [US1] Create module directory `ai-book/docs/module-1` for "ROS 2".
- [x] T008 [US1] Create module directory `ai-book/docs/module-2` for "Gazebo+Unity".
- [x] T009 [US1] Create module directory `ai-book/docs/module-3` for "NVIDIA Isaac".
- [x] T010 [US1] Create module directory `ai-book/docs/module-4` for "VLA Systems".
- [x] T011 [P] [US1] Create placeholder chapter `ai-book/docs/module-1/chapter-1.md`.
- [x] T012 [P] [US1] Create placeholder lesson `ai-book/docs/module-1/lesson-1-1.md`.
- [x] T013 [P] [US1] Create placeholder lesson `ai-book/docs/module-1/lesson-1-2.md`.
- [x] T014 [P] [US1] Create placeholder lesson `ai-book/docs/module-1/lesson-1-3.md`.
- [x] T015 [P] [US1] Create placeholder chapter `ai-book/docs/module-2/chapter-2.md`.
- [x] T016 [P] [US1] Create placeholder lesson `ai-book/docs/module-2/lesson-2-1.md`.
- [x] T017 [P] [US1] Create placeholder lesson `ai-book/docs/module-2/lesson-2-2.md`.
- [x] T018 [P] [US1] Create placeholder lesson `ai-book/docs/module-2/lesson-2-3.md`.
- [x] T019 [P] [US1] Create placeholder chapter `ai-book/docs/module-3/chapter-3.md`.
- [x] T020 [P] [US1] Create placeholder lesson `ai-book/docs/module-3/lesson-3-1.md`.
- [x] T021 [P] [US1] Create placeholder lesson `ai-book/docs/module-3/lesson-3-2.md`.
- [x] T022 [P] [US1] Create placeholder lesson `ai-book/docs/module-3/lesson-3-3.md`.
- [x] T023 [P] [US1] Create placeholder chapter `ai-book/docs/module-4/chapter-4.md`.
- [x] T024 [P] [US1] Create placeholder lesson `ai-book/docs/module-4/lesson-4-1.md`.
- [x] T025 [P] [US1] Create placeholder lesson `ai-book/docs/module-4/lesson-4-2.md`.
- [x] T026 [P] [US1] Create placeholder lesson `ai-book/docs/module-4/lesson-4-3.md`.
- [x] T027 [US1] Populate `ai-book/sidebars.js` with the full navigation structure for all modules, chapters, and lessons.

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently. The basic site structure is navigable.

---

## Phase 4: User Story 2 - Access Hands-On Lessons (Priority: P2)

**Goal**: As a learner, I want to access hands-on lessons with clear objectives, activities, and practice tasks, so that I can apply the concepts I've learned.

**Independent Test**: A lesson page (e.g., `lesson-1-1.md`) can be opened, and it contains all the required sections (objectives, concept summary, real-world context, an activity, technical notes, a practice task, reflection, and resources).

### Implementation for User Story 2

- [x] T028 [P] [US2] Populate content for `ai-book/docs/module-1/lesson-1-1.md` with all required sections.
- [x] T029 [P] [US2] Populate content for `ai-book/docs/module-1/lesson-1-2.md` with all required sections.
- [x] T030 [P] [US2] Populate content for `ai-book/docs/module-1/lesson-1-3.md` with all required sections.
- [x] T031 [P] [US2] Populate content for `ai-book/docs/module-2/lesson-2-1.md` with all required sections.
- [x] T032 [P] [US2] Populate content for `ai-book/docs/module-2/lesson-2-2.md` with all required sections.
- [x] T033 [P] [US2] Populate content for `ai-book/docs/module-2/lesson-2-3.md` with all required sections.
- [x] T034 [P] [US2] Populate content for `ai-book/docs/module-3/lesson-3-1.md` with all required sections.
- [x] T035 [P] [US2] Populate content for `ai-book/docs/module-3/lesson-3-2.md` with all required sections.
- [x] T036 [P] [US2] Populate content for `ai-book/docs/module-3/lesson-3-3.md` with all required sections.
- [x] T037 [P] [US2] Populate content for `ai-book/docs/module-4/lesson-4-1.md` with all required sections.
- [x] T038 [P] [US2] Populate content for `ai-book/docs/module-4/lesson-4-2.md` with all required sections.
- [x] T039 [P] [US2] Populate content for `ai-book/docs/module-4/lesson-4-3.md` with all required sections.
- [x] T040 [P] [US2] Create asset folder `ai-book/static/assets/module-1`.
- [x] T041 [P] [US2] Create asset folder `ai-book/static/assets/module-2`.
- [x] T042 [P] [US2] Create asset folder `ai-book/static/assets/module-3`.
- [x] T043 [P] [US2] Create asset folder `ai-book/static/assets/module-4`.
- [x] T044 [US2] Create capstone project file `ai-book/docs/capstone-project.md` and add it to sidebars.js.

**Checkpoint**: At this point, User Story 2 is complete. All lessons have their content structure, and the capstone project page exists.

---

## Phase 5: User Story 3 - Track Project History (Priority: P3)

**Goal**: As a project contributor, I want to view a history of changes and contributions to the textbook, so that I can understand the project's evolution.

**Independent Test**: The `history.md` page can be opened, and it contains a timeline of changes.

### Implementation for User Story 3

- [x] T045 [US3] Create `ai-book/docs/history.md`.
- [x] T046 [US3] Add initial timeline content to `ai-book/docs/history.md`.
- [x] T047 [US3] Add `history.md` to `ai-book/sidebars.js`.

**Checkpoint**: All user stories should now be independently functional.

---

## Phase N: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories.

- [x] T048 Populate content for all `chapter-x.md` introduction files.
- [x] T049 Review and refine content for all lessons.
- [ ] T050 Validate the entire site builds and runs without errors using `npm run build`.
- [ ] T051 Perform a final review against `quickstart.md` to ensure setup instructions are accurate.

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately.
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories.
- **User Stories (Phase 3+)**: All depend on Foundational phase completion.
  - User stories can then proceed sequentially in priority order (US1 → US2 → US3).
- **Polish (Final Phase)**: Depends on all user stories being complete.

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2).
- **User Story 2 (P2)**: Depends on User Story 1 to have the file structure in place.
- **User Story 3 (P3)**: Depends on User Story 1 to have the basic site structure.

### Within Each User Story

- Follow the task order as specified. Tasks marked with [P] can be executed in parallel.

### Parallel Opportunities

- **Phase 3 (US1)**: Creating placeholder files (T011-T026) can be done in parallel after the directories are created.
- **Phase 4 (US2)**: Populating lesson content (T028-T039) and creating asset folders (T040-T043) can be done in parallel.

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational
3. Complete Phase 3: User Story 1
4. **STOP and VALIDATE**: Test User Story 1 independently. The site should be navigable with placeholder pages.

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready.
2. Add User Story 1 → Test independently → MVP is a navigable site skeleton.
3. Add User Story 2 → Test independently → Site now has lesson content.
4. Add User Story 3 → Test independently → Site now has a history page.
5. Complete Polish Phase → Final validation and release.
