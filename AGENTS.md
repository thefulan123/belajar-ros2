# AGENTS.md — Multi-Agent Collaboration Rules

This file defines how AI agents should behave when working on this project.

## Project Type

Educational ROS2 learning repository for beginners.

## Core Principles

1. **Clarity over cleverness** — Code must be readable by ROS2 beginners.
2. **Teach while building** — Every file must include educational comments.
3. **Log everything** — Every meaningful action must be logged to `logs/agent-log.md`.
4. **Never overwrite carelessly** — Read existing code before editing.
5. **Dual language** — README/docs use Indonesian + English side by side.

## Directory Structure

```
Learn ROS2 from Scratch/
├── AGENTS.md              # AI agent rules
├── README.md              # Project overview (dual language)
├── .gitignore
├── explore/               # TRACK 1: Standalone Python files
│   ├── 01-minimal-node/   #   Run: python3 filename.py
│   ├── 02-pub-sub/        #   No build system needed
│   ├── 03-service/
│   ├── 04-action/
│   ├── 05-custom-msg/
│   └── 06-launch-params/
├── src/                   # TRACK 2: ROS2 colcon workspace
│   └── (packages will be added later)
├── launch/                # Launch files
├── config/                # YAML config files
├── scripts/               # Helper scripts (source_ros.sh, etc.)
├── docs/                  # Documentation
│   └── ERRORS.md          # Troubleshooting guide
├── logs/
│   └── agent-log.md       # Action log
└── tests/                 # Test files
```

## Dual-Track System

- **explore/** — Each folder is independent and runnable with `python3 filename.py`.
  Learner focuses on ONE concept at a time.
- **src/** — Proper ROS2 packages built with colcon.
  All nodes combined for full system integration.
- Topics/services with the SAME name automatically connect across both tracks.

## Logging Rules

Every meaningful action MUST append to `logs/agent-log.md` with:

- Timestamp
- Agent name
- Task description
- Files changed
- Reason
- Implementation details
- Result (success / partial / failed)
- Testing
- Next recommendation

## ROS2 Conventions

- Node names: lowercase_with_underscore (e.g., `talker_node`, `listener_node`)
- Topic names: lowercase_with_underscore (e.g., `/chatter`, `/robot_velocity`)
- Service names: descriptive verbs (e.g., `/add_two_ints`, `/reset_odometry`)
- One responsibility per node

## Forbidden Actions

- Deleting core folders
- Mass renaming files
- Changing dependencies recklessly
- Rewriting architecture without reason
- Creating duplicate nodes
- Hardcoding machine-specific paths
- Adding unnecessary complexity
- Claiming success without validation

## Decision Priority

1. System stability
2. Correct ROS2 communication
3. Readability
4. Educational clarity
5. Modularity
6. Performance
7. Refactoring aesthetics

## TODO Format

```
# TODO(agent-name):
# What needs to be done and why
```
