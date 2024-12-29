from agents import (GuardAgent, ClassificationAgent, 
                    DetailsAgent,
                    AgentProtocol,
                    RecommendationAgent,
                    OrderTakingAgent)
import os
from typing import Dict

import pathlib
folder_path = pathlib.Path(__file__).parent.resolve()



def main():
    
    gaurd_agent = GuardAgent()
    classification_agent = ClassificationAgent()
    
    recommendation_agent = RecommendationAgent(
                                    os.path.join(folder_path, 'recommendation_object/apriori_recommendations.json'),
                                    os.path.join(folder_path, 'recommendation_object/popularity_recommedation.csv'),
                                )
    agent_dict : Dict[str, AgentProtocol] = {
        "details_agent":DetailsAgent(),
        "recommendation_agent" : recommendation_agent,
        "order_taking_agent": OrderTakingAgent(recommendation_agent)
    }
    
    messages = []
    while True:
        os.system('cls' if os.name == 'nt' else 'clear')
        print("\n\nPrint Messages ...............")
        for message in messages:
            print(f"{message['role'].capitalize()}: {message['content']}")
 
        # Get user input
        prompt = input("User: ")
        messages.append({"role": "user", "content": prompt})
        
        
        # Get gaurd agent's response
        guard_agent_response = gaurd_agent.get_response(messages)
        if guard_agent_response["memory"]["guard_decision"] == "not allowed":
            messages.append(guard_agent_response)
            print('messages after gaurd response', messages)
            continue 
        
        # Get ClassificationAgent's response
        classification_agent_response = classification_agent.get_response(messages)
        chosen_agent=classification_agent_response["memory"]["classification_decision"]
       
        
        # Get the chosen agent's response
       
        agent = agent_dict[chosen_agent]
        response = agent.get_response(messages)
        
       
        
        messages.append(response)


if __name__ == "__main__":
    main()
     
    