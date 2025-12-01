# My Kiro Development Experience: Building the AWS Cost Forensics Agent

## Project Overview

This document captures my experience using Kiro to build the **Money Spender Agent** - an AWS spending forensics tool that reverse-engineers what wasteful AWS resources were likely deployed based on spending amounts and efficiency levels. The project uses the Strands Agents framework with Amazon Bedrock and demonstrates a complete AI-powered development lifecycle.

---

## 1. Building from Scratch: The AI-Powered Development Lifecycle (AIDLC)

### What is AIDLC?

AIDLC stands for **AI-Powered Development Lifecycle** - a methodology for building software projects iteratively with AI assistance. Rather than traditional waterfall or agile approaches, AIDLC leverages conversational AI to move fluidly through:

- **Analyze**: Understanding the problem space
- **Ideate**: Exploring solutions and approaches  
- **Design**: Creating structured specifications
- **Launch**: Implementing the solution
- **Check**: Validating and iterating

### My AIDLC Journey

#### Starting with High-Level Ideas

I began with a simple concept: "I want to build an agent that figures out what AWS resources someone deployed based on how much they spent." From this seed, Kiro helped me:

1. **Refine the concept** through conversation
2. **Identify key requirements** I hadn't considered
3. **Structure the problem** into manageable pieces
4. **Move from idea to executable spec**

#### The "Spec Moment" - From Idea to Design

The breakthrough came when Kiro helped me transition from loose ideas to **structured specifications**. Instead of jumping straight to code, we created:

- **`requirements.md`**: 8 detailed requirements with acceptance criteria
- **`design.md`**: Architecture, components, data models, and 13 correctness properties
- **`tasks.md`**: Step-by-step implementation plan with property-based tests

This spec-driven approach meant I had a clear roadmap before writing a single line of code.

---

## 2. The Most Impressive Code Generation: Strands Agent with MCP

### The Challenge: Getting Strands Agents API Right

Building a Strands agent requires understanding:
- The correct API syntax for agent creation
- How to configure system prompts effectively
- How structured output works with Pydantic models
- Integration with Amazon Bedrock

### How Kiro + MCP Solved It

**MCP (Model Context Protocol)** was the game-changer. Kiro used the **Strands Agents MCP server** to:

1. **Reference live documentation** about Strands APIs
2. **Get accurate syntax** for agent configuration
3. **Understand structured output patterns** with Pydantic
4. **Generate working code on the first try**

### The Result: `money_spender_aws_agent.py`

Kiro generated a complete agent implementation with:

```python
def create_money_spender_agent(
    *,
    model_id: Optional[str] = None,
) -> Agent:
    """Create a Money Spender agent that generates AWS cloud spending plans."""
    
    system_prompt = (
        "You are an AWS Cloud Cost Forensics Agent..."
        # Detailed prompt with efficiency levels, AWS services, pricing
    )
    
    agent = Agent(
        name="money_spender_agent",
        system_prompt=system_prompt,
        model=model_id or DEFAULT_MODEL_ID,
    )
    
    return agent
```

**What made this impressive:**
- The system prompt was comprehensive (200+ lines) with realistic AWS pricing
- Proper use of `structured_output_model` parameter
- Correct handling of Bedrock model IDs
- All generated from conversational requirements

---

## 3. Key "Aha Moments" During Development

### Aha #1: Requirements Articulation

**The Problem**: I was facing import issues and wasn't sure how to structure the project.

**The Breakthrough**: Kiro helped me articulate requirements I hadn't fully thought through, especially around:
- **System prompts**: How detailed should they be? What examples to include?
- **Input validation**: What edge cases exist for currency parsing?
- **Output structure**: How to format the forensic analysis?

By asking clarifying questions, Kiro helped me discover requirements like:
- "The agent should support 4 efficiency levels with specific waste patterns"
- "Cost breakdown must sum to input amount within 5% tolerance"
- "Services should include start_day and end_day for timeline tracking"

### Aha #2: Library Syntax Issues

**The Problem**: I was struggling with Strands Agents API syntax and Pydantic integration.

**The Solution**: Kiro used MCP to reference Strands documentation and:
- Found the correct `structured_output_model` parameter
- Showed how to access `result.structured_output`
- Replaced my manual JSON parsing with native structured output
- Fixed import statements and type hints

### Aha #3: Missing Requirements and Edge Cases

**The Discovery**: Through conversation, Kiro identified edge cases I hadn't considered:
- What if the user enters lowercase stupidity levels? (Added fuzzy matching)
- What if services start/stop mid-timeline? (Added start_day/end_day fields)
- What if the LLM returns costs that don't sum correctly? (Added validation)
- How to handle both $ and ₹ currencies? (Added currency parsing)

These became formal acceptance criteria in the requirements document.

---

## 4. The Spec-to-Code Workflow

### How I Structured My Spec

The spec consisted of three interconnected documents:

#### 1. **requirements.md** - The "What"
- 8 user stories with acceptance criteria
- Clear, testable requirements
- Example: "WHEN a user provides a spending amount in dollars or rupees, THE Agent SHALL parse and normalize the currency value"

#### 2. **design.md** - The "How"  
- Architecture diagrams
- Component interfaces
- 13 correctness properties for testing
- Error handling strategies
- Example property: "For any valid currency string containing $ or ₹ symbols, parsing should extract the correct numeric amount"

#### 3. **tasks.md** - The "Steps"
- 10 implementation tasks
- Each task linked to requirements
- Property tests mapped to tasks
- Checkboxes for tracking progress

### How Spec-Driven Development Improved My Process

**Before Specs (Traditional Approach):**
- Jump into coding with vague ideas
- Discover requirements mid-implementation
- Refactor constantly as understanding evolves
- Unclear when "done"

**With Specs (AIDLC Approach):**
- ✅ **Clarity**: Knew exactly what to build before coding
- ✅ **Confidence**: Requirements validated upfront
- ✅ **Efficiency**: Less refactoring, more focused implementation
- ✅ **Testability**: Properties defined before code
- ✅ **Communication**: Spec serves as documentation

### The Implementation Flow

1. **Write requirements** with Kiro's help (captured edge cases)
2. **Design architecture** and correctness properties
3. **Break into tasks** with clear dependencies
4. **Implement task-by-task** with Kiro generating code
5. **Validate against properties** (planned for future)

---

## 5. Steering Files: Project Knowledge Base

Beyond the spec, I created **steering files** that Kiro automatically includes in context:

### `project-overview.md`
- Project structure and key components
- Usage examples
- Development guidelines
- Testing checklist

### `coding-standards.md`
- Python style guide
- Pydantic patterns
- Error handling conventions
- Strands agent best practices

### `aws-services-guide.md`
- AWS service catalog with pricing
- Efficiency level guidelines
- Realistic waste patterns
- Cost calculation formulas

**The Impact**: These steering files meant Kiro consistently:
- Followed project conventions
- Used realistic AWS pricing
- Maintained code style
- Referenced correct patterns

---

## 6. Key Takeaways for Other Developers

### What Worked Exceptionally Well

1. **MCP for Framework Documentation**
   - Kiro accessed live Strands Agents docs via MCP
   - Generated correct API usage without trial-and-error
   - Saved hours of documentation reading

2. **Spec-First Development**
   - Requirements → Design → Tasks → Code
   - Clear acceptance criteria prevented scope creep
   - Correctness properties provide testing roadmap

3. **Iterative Refinement**
   - Started with high-level idea
   - Kiro asked clarifying questions
   - Discovered edge cases through conversation
   - Formalized learnings into specs

4. **Steering Files as Context**
   - Project guidelines always available
   - Consistent code generation
   - Reduced need to repeat instructions

### Challenges and Solutions

| Challenge | Solution |
|-----------|----------|
| Import syntax errors | Kiro used MCP to reference correct APIs |
| Vague requirements | Conversational refinement → formal acceptance criteria |
| Complex system prompts | Kiro generated detailed prompts with examples |
| Structured output confusion | MCP docs showed `structured_output_model` pattern |
| Missing edge cases | Kiro identified through "what if" questions |

### Recommendations for New Kiro Users

1. **Start with conversation, not code**
   - Describe your idea in plain language
   - Let Kiro ask clarifying questions
   - Refine requirements before implementation

2. **Use specs for complex projects**
   - Requirements → Design → Tasks
   - Define correctness properties upfront
   - Link tasks to requirements

3. **Leverage MCP servers**
   - Install framework-specific MCP servers
   - Let Kiro reference live documentation
   - Avoid API syntax guesswork

4. **Create steering files early**
   - Project overview
   - Coding standards
   - Domain-specific knowledge (like AWS pricing)

5. **Embrace iteration**
   - First pass won't be perfect
   - Refine specs as understanding grows
   - Update steering files with learnings

---

## 7. Project Artifacts

### Final Project Structure

```
.
├── agent/
│   ├── main.py                      # CLI with interactive mode
│   ├── money_spender_aws_agent.py   # Strands agent implementation
│   ├── schema.py                    # Pydantic models
│   └── requirements.txt             # Dependencies
├── .kiro/
│   ├── specs/aws-cost-forensics/
│   │   ├── requirements.md          # 8 requirements, 40+ criteria
│   │   ├── design.md                # Architecture + 13 properties
│   │   └── tasks.md                 # 10 implementation tasks
│   └── steering/
│       ├── project-overview.md      # Project guide
│       ├── coding-standards.md      # Style conventions
│       └── aws-services-guide.md    # Domain knowledge
└── README.md                        # User documentation
```

### Lines of Code Generated

- **Agent implementation**: ~200 lines
- **CLI interface**: ~150 lines  
- **Schema definitions**: ~50 lines
- **System prompt**: ~200 lines
- **Documentation**: ~500 lines

**Total**: ~1,100 lines of production-quality code and documentation

### Time Investment

- **Spec creation**: ~2 hours (with Kiro's help)
- **Implementation**: ~1 hour (Kiro generated most code)
- **Refinement**: ~1 hour (fixing edge cases)

**Total**: ~4 hours for a complete, documented, spec-driven project

---

## 8. Conclusion

Building the AWS Cost Forensics Agent with Kiro demonstrated the power of **AI-Powered Development Lifecycle (AIDLC)**. By combining:

- Conversational requirement gathering
- Spec-driven development
- MCP-powered documentation access
- Steering files for consistency

I was able to build a sophisticated Strands agent with structured output, comprehensive error handling, and detailed documentation in a fraction of the time traditional development would require.

The key insight: **Kiro is most powerful when you invest in structure upfront** (specs, steering files) rather than jumping straight to code. The spec becomes a contract between you and the AI, ensuring consistent, high-quality output.

---

## Appendix: Example Interactions

### Initial Conversation (Analyze Phase)

**Me**: "I want to build an agent that figures out what AWS resources someone deployed based on spending"

**Kiro**: "Interesting! Let me ask some clarifying questions:
- What inputs should the agent accept?
- Should it consider time periods?
- How accurate should the forensics be?
- What output format do you want?"

### Requirement Refinement (Ideate Phase)

**Me**: "It should take an amount and tell me what services were used"

**Kiro**: "Got it. Some edge cases to consider:
- Multiple currencies?
- Different efficiency levels (wasteful vs optimized)?
- Should costs sum exactly to the input?
- Timeline tracking for when services started/stopped?"

### Implementation (Launch Phase)

**Me**: "Generate the agent with structured output"

**Kiro**: *[Uses Strands MCP]* "Here's the agent with proper structured_output_model usage..."

---

**Document Version**: 1.0  
**Project**: AWS Cost Forensics Agent  
**Date**: November 30, 2025  
**Author**: [Your Name]  
**Tool**: Kiro AI IDE
