import os
from crewai.flow import Flow, start, listen
from crewai import Agent, Task, Crew, LLM

# ---- LLM Configuration ----
def get_llm():
    azure_key = os.getenv("AZURE_API_KEY")
    openai_key = os.getenv("OPENAI_API_KEY")
    
    if azure_key and os.getenv("AZURE_API_BASE"):
        print("Using Azure OpenAI")
        return LLM(
            model=f"azure/{os.getenv('AZURE_DEPLOYMENT_NAME')}",
            base_url=os.getenv("AZURE_API_BASE"),
            api_key=azure_key,
            api_version=os.getenv("AZURE_API_VERSION"),
        )
    else:
        raise ValueError("No valid API keys found. Set either AZURE_API_KEY or OPENAI_API_KEY")

llm = get_llm()

# ---- Agents ----
venue_agent = Agent(
    role="Venue Coordinator",
    goal="Find suitable venues for events",
    backstory="You are an experienced venue coordinator with extensive knowledge of event spaces. You provide practical venue recommendations with accurate details.",
    llm=llm,
    verbose=True
)

logistics_agent = Agent(
    role="Logistics Manager",
    goal="Arrange catering & equipment for events",
    backstory="You are a detail-oriented logistics manager with years of experience. You provide practical, cost-effective solutions for event operations.",
    llm=llm,
    verbose=True
)

marketing_agent = Agent(
    role="Marketing Specialist",
    goal="Create effective event marketing strategies",
    backstory="You are a creative marketing specialist who develops practical, budget-conscious marketing plans with measurable outcomes.",
    llm=llm,
    verbose=True
)

# ---- Flow ----
class EventPlannerFlow(Flow):
    
    def __init__(self):
        super().__init__()
        self.venue_result = ""
        self.logistics_result = ""
        self.marketing_result = ""

    @start()
    def venue_task(self):
        """Find a suitable venue"""
        event_city = self.state.get('event_city')
        event_topic = self.state.get('event_topic')
        expected_participants = self.state.get('expected_participants')
        tentative_date = self.state.get('tentative_date')
        
        task = Task(
            description=(
                f"Find a suitable venue in {event_city} for '{event_topic}' "
                f"that can accommodate {expected_participants} people on {tentative_date}. "
                f"Provide: venue name, address, capacity, key amenities, and estimated cost per day."
            ),
            expected_output="A detailed venue recommendation with name, address, capacity, amenities, and cost",
            agent=venue_agent
        )
        
        crew = Crew(
            agents=[venue_agent],
            tasks=[task],
            verbose=False
        )
        result = crew.kickoff()
        self.venue_result = result.raw

    @listen(venue_task)
    def logistics_task(self, venue_info):
        """Plan logistics"""
        task = Task(
            description=(
                f"Based on this venue: {venue_info}\n\n"
                f"Plan the logistics including:\n"
                f"1. Catering options (breakfast, lunch, refreshments)\n"
                f"2. AV equipment needed\n"
                f"3. Furniture and seating arrangements\n"
                f"4. Vendor recommendations with estimated costs"
            ),
            expected_output="Comprehensive logistics plan with vendor recommendations and cost estimates",
            agent=logistics_agent
        )
        
        crew = Crew(
            agents=[logistics_agent],
            tasks=[task],
            verbose=False
        )
        result = crew.kickoff()
        self.logistics_result = result.raw

    @listen(logistics_task)
    def marketing_task(self, logistics_info):
        """Create marketing plan"""
        task = Task(
            description=(
                f"Create a marketing strategy considering these logistics: {logistics_info}\n\n"
                f"Include:\n"
                f"1. Target channels (social media, email, partnerships)\n"
                f"2. Content strategy and timeline\n"
                f"3. Estimated reach and engagement goals\n"
                f"4. Marketing budget breakdown"
            ),
            expected_output="Complete marketing plan with channels, timeline, reach estimates, and budget",
            agent=marketing_agent
        )
        
        crew = Crew(
            agents=[marketing_agent],
            tasks=[task],
            verbose=False
        )
        result = crew.kickoff()
        self.marketing_result = result.raw



# ---- Run function ----
def run_flow(inputs: dict):
    try:
        flow = EventPlannerFlow()
        flow.kickoff(inputs=inputs)
        
        return {
            "status": "success",
            "venue_recommendation": flow.venue_result,
            "logistics_plan": flow.logistics_result,
            "marketing_plan": flow.marketing_result,
        }
    except Exception as e:
        return {
            "status": "error",
            "message": f"Flow execution failed: {str(e)}",
            "error_type": type(e).__name__
        }