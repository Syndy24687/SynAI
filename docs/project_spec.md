# SynAI Architecture Specification

## 1. High-level architecture

SynAI should be implemented as a layered, offline-first desktop application with clear separation between user interaction, orchestration, AI services, automation, memory, and extensibility.

### Core architectural style

- A thin UI layer handles presentation and user events.
- A central orchestration layer interprets requests, routes work, and coordinates services.
- Domain services encapsulate business logic without depending on UI concerns.
- Infrastructure adapters connect to Ollama, SQLite, speech pipelines, browser automation, and desktop automation.
- Plugins extend behavior through well-defined contracts rather than modifying core code.

### Recommended runtime layers

1. Presentation layer
   - Desktop shell and chat/voice interfaces.
   - User input capture and output rendering.
   - Session state visualization and simple system feedback.

2. Orchestration layer
   - Intent recognition and task planning.
   - Tool selection and workflow execution.
   - Event routing and state transitions.

3. Intelligence layer
   - Local LLM integration through Ollama.
   - Speech-to-text and text-to-speech services.
   - Prompt composition and response formatting.

4. Automation layer
   - Browser automation for web interaction.
   - Desktop automation for local application control.
   - Safe command execution for repeated tasks.

5. Memory layer
   - Conversation memory.
   - Episodic and semantic memory.
   - Retrieval and summarization services.

6. Extension layer
   - Plugin discovery, registration, and execution.
   - Capability-based hooks and permission boundaries.

### Data flow

1. User input arrives through voice or chat.
2. The orchestration layer classifies the request.
3. The planner decides whether to use AI reasoning, memory, automation, or a plugin.
4. The selected service executes the action.
5. Results are persisted to memory and returned to the user.

### Architectural principles

- Follow SOLID principles strictly.
- Prefer composition over inheritance.
- Use dependency injection for service dependencies.
- Keep modules small and focused on a single concern.
- Avoid circular imports by depending on abstractions and stable interfaces.
- Favor maintainability, testability, and offline operation over complexity.

---

## 2. Responsibilities of every folder

### root

- Maintain project bootstrap and top-level entry points.
- Keep runtime configuration, scripts, and documentation discoverable.

### main.py

- Serve as the single application entry point.
- Construct the application container and start the runtime.
- Avoid embedding business logic in this file.

### src/

- Contain the application source code organized by technical responsibility.
- Keep the package structure explicit and dependency-friendly.

### src/ai/

- Own all AI-facing services.
- Manage LLM access, prompt construction, speech processing, and content generation.

### src/browser/

- Own browser automation behaviors and browser session management.
- Provide a stable interface for web tasks without leaking browser-specific details into the core system.

### src/config/

- Own configuration loading, validation, and environment-specific defaults.
- Keep settings strongly typed and centralised.

### src/core/

- Own orchestration, shared abstractions, domain services, and application wiring.
- This should remain the architectural backbone of the system.

### src/memory/

- Own persistent and transient memory systems.
- Manage structured storage for conversations, summaries, facts, and retrieval indexes.

### src/plugins/

- Own plugin discovery, metadata, lifecycle management, and execution contracts.
- Keep plugin infrastructure independent from core business logic.

### src/speech/

- Own voice capture, audio playback, and speech pipeline orchestration.
- Convert audio streams to text and text to audio in a reusable way.

### src/system/

- Own desktop automation and operating-system integration.
- Keep OS-specific logic isolated from the rest of the application.

### src/ui/

- Own all user interface components and user interaction flows.
- Keep UI code free of business rules whenever possible.

### src/utils/

- Own shared helpers that do not belong to a specific domain.
- Include paths, logging helpers, timing utilities, serialization, and retry logic.

### config/

- Store environment-specific configuration files and example templates.
- Keep secrets out of version control and reference them through environment variables.

### data/

- Store runtime data that is produced or consumed locally.
- Include caches, local indexes, and durable working files.

### docs/

- Contain architecture, design, and product documentation.
- Maintain a single source of truth for planning decisions.

### logs/

- Store runtime log files and diagnostic output.
- Keep log retention and rotation policies explicit.

### tests/

- Contain unit, integration, and contract tests.
- Validate behavior of core services and interfaces.

### assests/

- Store non-code resources such as icons, sound files, and UI assets.

---

## 3. Responsibilities of every Python module

The following modules are the recommended responsibility boundaries for the project.

### main.py

- Application entry point.
- Creates the dependency container and startup services.
- Starts the main event loop or UI runtime.

### src/core/app.py

- Instantiates the main application object.
- Wires together services, repositories, adapters, and UI components.

### src/core/container.py

- Defines the dependency injection container.
- Registers concrete implementations for abstractions.

### src/core/interfaces.py

- Declares stable protocols and abstractions for services.
- Prevents circular dependencies by defining contracts in one place.

### src/core/orchestrator.py

- Coordinates user requests, tool selection, and workflow execution.
- Acts as the central decision-making coordinator.

### src/core/session_manager.py

- Tracks active sessions, user context, and conversation state.
- Owns lifecycle operations for session continuity.

### src/core/events.py

- Defines event types and event bus behavior.
- Enables loose coupling between subsystems.

### src/core/exceptions.py

- Defines domain-specific exceptions.
- Standardizes error semantics across the application.

### src/ai/llm_client.py

- Wraps communication with Ollama.
- Encapsulates request formatting, retries, and model selection.

### src/ai/prompt_builder.py

- Builds system prompts, task prompts, and context-aware instructions.
- Keeps prompt logic separate from execution logic.

### src/ai/intent_classifier.py

- Identifies the intent of incoming requests.
- Maps intent categories to capabilities or workflows.

### src/ai/speech_to_text.py

- Wraps the speech recognition pipeline.
- Converts captured audio into structured text input.

### src/ai/text_to_speech.py

- Wraps text-to-speech generation.
- Provides a stable interface for voice responses.

### src/ai/embedding_service.py

- Generates embeddings or lightweight semantic representations for memory retrieval.
- Keeps retrieval logic independent from storage details.

### src/browser/driver.py

- Provides a browser automation facade.
- Abstracts the concrete browser automation backend.

### src/browser/actions.py

- Defines browser-level operations such as click, type, navigate, and wait.
- Keeps action definitions reusable across tasks.

### src/browser/task_runner.py

- Executes browser automation plans and interprets results.
- Converts browser tasks into structured outcomes.

### src/speech/audio_pipeline.py

- Manages microphone and speaker operations.
- Coordinates recording, buffering, and playback.

### src/system/desktop.py

- Wraps desktop automation actions such as opening apps or sending shortcuts.
- Avoids leaking OS-specific behavior into core services.

### src/system/commands.py

- Executes safe system commands through a controlled abstraction.
- Provides centralized validation and error handling.

### src/memory/models.py

- Declares memory record schemas and persistence entities.
- Keeps storage contracts explicit.

### src/memory/repository.py

- Abstracts data access for memory operations.
- Enables different storage backends if needed.

### src/memory/conversation_store.py

- Handles conversation history and transcript persistence.
- Supports retrieval by session and time.

### src/memory/semantic_store.py

- Stores semantic memory and retrieval indexes.
- Supports similarity-based lookup for relevant prior context.

### src/memory/summary_service.py

- Produces summaries for long conversations or repeated tasks.
- Keeps memory size manageable.

### src/plugins/contracts.py

- Declares plugin interfaces and lifecycle hooks.
- Defines the extension contract for third-party modules.

### src/plugins/manager.py

- Discovers, loads, validates, and registers plugins.
- Enforces a consistent lifecycle.

### src/plugins/registry.py

- Stores active plugins and their registered capabilities.
- Supports discovery of available plugin actions.

### src/config/settings.py

- Loads settings from environment variables, config files, and defaults.
- Validates them at startup.

### src/config/schema.py

- Defines configuration models and validation rules.
- Keeps configuration strongly typed.

### src/ui/app_window.py

- Owns the main desktop window shell.
- Coordinates top-level views and state.

### src/ui/chat_view.py

- Renders chat history and user/assistant messages.
- Keeps view logic separate from business behavior.

### src/ui/voice_view.py

- Handles voice status, recording state, and live feedback.
- Keeps voice UI concerns isolated.

### src/ui/agent_view.py

- Displays automation activity, task progress, and agent reasoning state.
- Makes runtime transparency available without mixing with orchestration logic.

### src/utils/logging.py

- Centralizes logging configuration and helper functions.
- Ensures consistent logger usage.

### src/utils/retry.py

- Provides reusable retry and backoff logic for transient failures.
- Keeps resilience behavior centralized.

### src/utils/paths.py

- Provides safe path handling for app data, config, and logs.
- Avoids scattered path logic.

---

## 4. Recommended package structure

```text
SynAI/
├── main.py
├── README.md
├── requirements.txt
├── assests/
├── config/
│   ├── defaults.toml
│   └── example.local.toml
├── data/
├── docs/
│   └── project_spec.md
├── logs/
├── src/
│   ├── ai/
│   │   ├── __init__.py
│   │   ├── llm_client.py
│   │   ├── prompt_builder.py
│   │   ├── intent_classifier.py
│   │   ├── speech_to_text.py
│   │   ├── text_to_speech.py
│   │   └── embedding_service.py
│   ├── browser/
│   │   ├── __init__.py
│   │   ├── driver.py
│   │   ├── actions.py
│   │   └── task_runner.py
│   ├── config/
│   │   ├── __init__.py
│   │   ├── settings.py
│   │   └── schema.py
│   ├── core/
│   │   ├── __init__.py
│   │   ├── app.py
│   │   ├── container.py
│   │   ├── interfaces.py
│   │   ├── orchestrator.py
│   │   ├── session_manager.py
│   │   ├── events.py
│   │   └── exceptions.py
│   ├── memory/
│   │   ├── __init__.py
│   │   ├── models.py
│   │   ├── repository.py
│   │   ├── conversation_store.py
│   │   ├── semantic_store.py
│   │   └── summary_service.py
│   ├── plugins/
│   │   ├── __init__.py
│   │   ├── contracts.py
│   │   ├── manager.py
│   │   └── registry.py
│   ├── speech/
│   │   ├── __init__.py
│   │   ├── audio_pipeline.py
│   │   └── voice_service.py
│   ├── system/
│   │   ├── __init__.py
│   │   ├── desktop.py
│   │   └── commands.py
│   ├── ui/
│   │   ├── __init__.py
│   │   ├── app_window.py
│   │   ├── chat_view.py
│   │   ├── voice_view.py
│   │   └── agent_view.py
│   └── utils/
│       ├── __init__.py
│       ├── logging.py
│       ├── retry.py
│       └── paths.py
├── tests/
│   ├── unit/
│   ├── integration/
│   └── contract/
└── .gitignore
```

---

## 5. Coding conventions

- Use Python 3.13-compatible syntax and features.
- Use type hints for every function parameter, return value, and variable where practical.
- Add docstrings to every public class and public function.
- Keep functions short and focused; prefer under 40 lines when practical.
- Use `snake_case` for functions and variables, `PascalCase` for classes.
- Use immutable configuration objects and value objects where appropriate.
- Prefer composition over inheritance.
- Favor interfaces and protocols for dependency injection.
- Keep modules narrow in responsibility and avoid cross-cutting concerns leaking into domain code.
- Use `from __future__ import annotations` to support forward references.
- Avoid `print()` entirely; use the logging framework.
- Keep third-party dependencies isolated behind adapters.
- Write tests alongside new services and interfaces.

---

## 6. Error-handling strategy

SynAI should fail safely, predictably, and transparently.

### Principles

- Catch exceptions at the boundary layer rather than deep inside business logic.
- Use specific exception types instead of broad fallback logic.
- Preserve user-friendly failure messages while logging technical details.
- Degrade gracefully when AI, speech, browser, or desktop services are unavailable.
- Keep offline-first behavior intact even when cloud-based dependencies are missing.

### Recommended approach

- Define a small set of domain exceptions such as `ConfigurationError`, `ServiceUnavailableError`, `PluginError`, and `AutomationError`.
- Wrap third-party integrations in adapter code so failures are normalized.
- Retry transient failures with backoff for network or local service interruptions.
- Provide a fallback path such as returning a helpful message or switching to a simpler workflow.
- Record diagnostic context with the exception for later troubleshooting.

---

## 7. Logging strategy

The system should use Python’s standard logging module consistently.

### Logging requirements

- Use module-specific loggers such as `logger = logging.getLogger(__name__)`.
- Support console and file output.
- Use structured log records where possible, including event type, component, session id, and correlation id.
- Keep log levels consistent: `DEBUG` for development, `INFO` for normal workflow, `WARNING` for recoverable issues, and `ERROR` for failures.
- Rotate log files to avoid unbounded growth.

### Recommended log destinations

- Console output during development.
- File logs under the logs directory in production.
- Optional diagnostics for debugging sessions and support scenarios.

### Privacy principles

- Avoid logging secrets, access tokens, or sensitive user content by default.
- Redact Personally Identifiable Information where needed.

---

## 8. Configuration strategy

Configuration should be centralized, validated, and environment-aware.

### Strategy

- Maintain default settings in a versioned defaults file.
- Allow environment-specific overrides using local config files or environment variables.
- Validate all settings at startup and fail fast on misconfiguration.
- Keep secrets in environment variables or a secure local secret store.

### Recommended configuration sources

1. Built-in defaults.
2. Environment variables.
3. Local configuration files for development and testing.
4. Optional secure secret providers for deployment scenarios.

### Recommended settings categories

- Application settings: app name, version, working directories.
- AI settings: model name, timeout, temperature, local service URL.
- Speech settings: input device, output device, sample rate.
- Automation settings: browser executable path, timeout policies, sandboxing behavior.
- Memory settings: storage path, retention policy, indexing mode.
- Plugin settings: enable/disable plugins, permission model, discovery paths.

---

## 9. Plugin strategy

Plugins should extend SynAI without forcing core changes.

### Plugin goals

- Add new capabilities without modifying the core orchestration engine.
- Support third-party extension while preserving reliability.
- Keep plugin execution isolated and auditable.

### Recommended plugin model

- Each plugin exposes a manifest describing name, version, capabilities, and permissions.
- Plugins implement a stable interface with lifecycle hooks such as `initialize`, `shutdown`, and `handle_request`.
- The plugin manager discovers plugins from a known directory and validates their metadata.
- Registered capabilities are exposed to the orchestrator through the plugin registry.
- Plugin execution should run with explicit permission checks and clear error handling.

### Safety controls

- Disable plugins by default unless explicitly approved.
- Enforce a permission model for browser, desktop, file, or network access.
- Prefer local-only execution for the first releases.
- Log plugin activity for debugging and trust review.

---

## 10. Development roadmap divided into milestones

### Milestone 1 — Foundation and architecture scaffolding

- Create the package structure and dependency injection container.
- Define abstractions for AI, memory, browser, speech, and desktop automation.
- Establish logging, configuration, and exception conventions.
- Create initial tests for configuration and core services.

### Milestone 2 — Core assistant experience

- Implement chat input and response flow.
- Connect the local LLM adapter through Ollama.
- Add basic session management and conversation persistence.
- Implement the first version of voice input and voice response.

### Milestone 3 — Automation capabilities

- Add browser automation actions and task execution.
- Add desktop automation wrappers for common local tasks.
- Create safe command execution and approval workflow patterns.
- Improve orchestrator routing for automation tasks.

### Milestone 4 — Memory and extensibility

- Implement memory storage, retrieval, and summarization.
- Add semantic memory and context recall workflow.
- Deliver the first plugin system with a built-in example plugin.
- Introduce plugin permissions and health monitoring.

### Milestone 5 — Reliability, polish, and release readiness

- Add comprehensive unit and integration tests.
- Improve error handling, recovery, and fallback behavior.
- Add performance monitoring, logging quality, and diagnostics.
- Prepare packaging, installation, and offline usage documentation.

---

## Final architectural recommendation

SynAI should be built as a modular, dependency-injected desktop application with a strong core orchestration layer and a plugin-friendly extension model. The initial focus should be on a stable local AI experience, reliable memory, and safe automation boundaries. This approach will preserve maintainability, support future growth, and align well with the offline-first and extensibility goals of the project.