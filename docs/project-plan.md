# Project Plan

## Fase 0

- [ ] Brainstorming
  - [ ] /analyst *brainstorm "Root Cause Analysis and Solution Design for Player Inactivity"
  - [ ] /analyst *brainstorm "User Flow Deviations & Edge Cases"
- [ ] Research
  - [ ] /analyst *research "Which AI library should we use for orchestrating LLM interactions?"
- [ ] Product Brief
  - [ ] /analyst *product-brief "Read the two brainstorming sessions the research session and the @proposal.md file, and create a product brief for the project."

## Fase 1

- [ ] Planning
  - [] /run-agent-task pm *prd
  - [ ] /run-agent-task pm *validate-prd
  - [ ] /run-agent-task ux-designer *create-ux-design {prompt / user-input-file}
  - [ ] /run-agent-task ux-designer *validate-ux-design {prompt / user-input-file}
  - [ ] /run-agent-task tea *framework {prompt / user-input-file}
  - [ ] /run-agent-task tea *ci {prompt / user-input-file}
  - [ ] /run-agent-task tea *test-design {prompt / user-input-file}

## Fase 2

- [ ] Solutioning
  - [ ] /run-agent-task architect *architecture {prompt / user-input-file}
  - [ ] /run-agent-task architect *validate-architecture {prompt / user-input-file}

## Fase 3

- [ ] Implementation
  - [ ] /run-agent-task sm *sprint-planning {prompt / user-input-file}
  - foreach epic in sprint planning:
    - [ ] /run-agent-task sm epic-tech-content {prompt / user-input-file}
    - [ ] /run-agent-task sm validate-epic-tech-content {prompt / user-input-file}
    - foreach story in epic:
      - [ ] /run-agent-task sm *create-story {prompt / user-input-file}
      - [ ] /run-agent-task sm *validate-create-story {prompt / user-input-file}
      - [ ] /run-agent-task sm *story-context {prompt / user-input-file}
      - [ ] /run-agent-task sm *validate-story-context {prompt / user-input-file}
      - [ ] /run-agent-task tea *validate-story-ready {prompt / user-input-file}
      - [ ] /run-agent-task dev *implement-story {prompt / user-input-file}
      - [ ] /run-agent-task dev *validate-story {prompt / user-input-file}
      - [ ] /run-agent-task tea *automate {prompt / user-input-file}
      - [ ] /run-agent-task tea *test-review {prompt / user-input-file}
    - [ ] /run-agent-task sm *retrospective {prompt / user-input-file}
