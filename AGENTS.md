# AGENTS.md — Multi-Agent Collaboration Rules

This file defines how AI agents should behave when working on this project.

## Project Type

Educational ROS2 learning repository for beginners.

## Core Principles

1. **Clarity over cleverness** — Code must be readable by ROS2 beginners.
2. **Teach while building** — Every file must include educational comments.
3. **Log everything** — Every meaningful action must be logged to `Dasar ROS2/logs/agent-log.md`.
4. **Never overwrite carelessly** — Read existing code before editing.
5. **Dual language** — README/docs use Indonesian + English side by side.

## Directory Structure

```
Learn ROS2 from Scratch/
├── AGENTS.md              # AI agent rules
├── README.md              # Project overview (dual language)
├── .gitignore
│
├── Dasar ROS2/            # LEVEL 1: Basic ROS2
│   ├── Materi.txt         #   Daftar topik
│   ├── modul/             #   Modul pembelajaran teori
│   │   ├── 01-sourcing.md
│   │   ├── 02-workspace.md
│   │   ├── 03-package.md
│   │   ├── 04-create-package.md
│   │   ├── 05-build-package.md
│   │   ├── 06-source-workspace.md
│   │   ├── 07-callback-event-timer.md
│   │   └── 08-micro-ros-arduino.md
│   ├── explore/           #   TRACK 1: Standalone Python files
│   │   ├── 01-minimal-node/   # Run: python3 filename.py
│   │   ├── 02-pub-sub/
│   │   ├── 03-service/
│   │   ├── 04-action/
│   │   ├── 05-custom-msg/
│   │   ├── 06-launch-params/
│   │   └── 07-arduino-uno/
│   ├── src/               #   TRACK 2: ROS2 colcon workspace
│   ├── launch/            #   Launch files
│   ├── config/            #   YAML config files
│   ├── scripts/           #   Helper scripts
│   ├── docs/              #   Documentation
│   │   ├── disclaimer.md
│   │   └── ERRORS.md
│   ├── logs/              #   Action log
│   │   └── agent-log.md
│   └── tests/             #   Test files
│
└── Menengah ROS2/         # LEVEL 2: (akan datang)
```

## Dual-Track System

- **Dasar ROS2/explore/** — Each folder is independent and runnable with `python3 filename.py`.
  Learner focuses on ONE concept at a time.
- **Dasar ROS2/src/** — Proper ROS2 packages built with colcon.
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
