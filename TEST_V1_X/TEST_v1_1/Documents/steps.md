rough dev steps:

1. start with enums. Only apply the Create function for now though. Create four enums at least.
2. design operation state for Create and the relevant responses, schemas
3. plan the lifecycle for a simple Create request
4. pipe function -> operation state trigger the planned lifecycle.
5. then handle responses, hook to a postgres docker just as a test.
