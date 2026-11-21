Source: LangChain documentation - Tools (docs.langchain.com/oss/python/langchain/tools)
License: see corpus/ATTRIBUTION.md

# Tools and Tool Calling

Tools are functions an agent can call to interact with the outside world, such as searching a database, running a calculation, or calling an API. Each tool has a name, a description, and a typed input schema.

Tool calling works in a loop. The model reads the request and the tool descriptions, decides a tool call is needed, emits the call with arguments, the application executes the function, and the result is returned to the model as context for the next step.

Clear tool descriptions matter as much as correct code. A model can only choose the right tool when each description states plainly what the tool does and when it should be used.

Tools should be scoped narrowly and treated as untrusted boundaries. Read-only tools are safer defaults, and write actions usually deserve validation, logging, or human approval.
