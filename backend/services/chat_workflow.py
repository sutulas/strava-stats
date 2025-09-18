from typing import List, Dict, Any, Optional, TypedDict
from langgraph.graph import StateGraph, START, END
# from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
import pandas as pd
import sys
import json
from openai import OpenAI
import os
import dotenv
from dataclasses import dataclass
from io import StringIO
import re

dotenv.load_dotenv()


client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


class WorkflowState(TypedDict):
    messages: List[Any]  # Can be List[Dict[str, Any]] or List[HumanMessage] or similar
    enhanced_query: Optional[str] = None
    df: pd.DataFrame
    chart_code: Optional[str] = None
    chart_output: Optional[str] = None
    overview: Optional[str] = None
    code: Optional[str] = None
    output: Optional[str] = None
    response: Optional[str] = None


class StravaWorkflow:
    def __init__(self):
        self.graph = self._build_workflow()

    def _build_workflow(self):

        workflow = StateGraph(WorkflowState)

        workflow.add_node("analyze_query", self._analyze_query)
        workflow.add_node("enhance_query", self._enhance_query)
        workflow.add_node("prepare_graphs", self._prepare_graphs)
        workflow.add_node("graph_data", self._graph_data)
        workflow.add_node("prepare_data", self._prepare_data)
        workflow.add_node("analyze_data", self._analyze_data)
        workflow.add_node("verify_graphs", self._verify_graphs)
        workflow.add_node("verify_code", self._verify_code)
        workflow.add_node("final_response", self._final_response)

        workflow.add_edge(START, "analyze_query")

        workflow.add_edge("analyze_query", "enhance_query")
        workflow.add_conditional_edges(
            "enhance_query",
            self._analyze_query_conditional,
            {
                "prepare_graphs": "prepare_graphs",
                "prepare_data": "prepare_data",
            }
        )

        workflow.add_edge("prepare_graphs", "verify_graphs")
        workflow.add_edge("prepare_data", "verify_code")

        workflow.add_edge("verify_graphs", "graph_data")
        workflow.add_edge("verify_code", "analyze_data")

        workflow.add_edge("graph_data", "final_response")
        workflow.add_edge("analyze_data", "final_response")


        workflow.add_edge("final_response", END)

        return workflow.compile()

    def get_graph(self):
        return self.graph

    def _analyze_query(self, state: WorkflowState) -> WorkflowState:
        print(state["messages"])
        last_message = state["messages"][-1]
        if isinstance(last_message, dict):
            query = last_message.get('content', '')
        else:
            query = getattr(last_message, 'content', str(last_message))
        print(f"Analyzing query: {query}")
        return state

    def _enhance_query(self, state: WorkflowState) -> WorkflowState:
        print("Enhancing query")
        last_message = state["messages"][-1]
        if isinstance(last_message, dict):
            query = last_message.get('content', '')
        else:
            query = getattr(last_message, 'content', str(last_message))
        prompt = f'''
        
        User query: {query}

        Overview: {state["overview"]}

        You are a data analysis expert. You are given a user query. You need to enhance the query to be more specific and accurate.
        You are part of a workflow where the next step will generate code to do data analysis or generate a chart using pandas or seaborn. 
        The next step is {"graph_data" if "chart" in query.lower() else "analyze_data"}.
        Add specifics to the query to help the code generation (ie what the X-axis should be, what columns to use, what operations should be done, and so on...)
        
        Return only the enhanced query, be concise not conversational.
        '''
        response = client.chat.completions.create(
            model="gpt-4.1",
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        enhanced_query = response.choices[0].message.content
        state["enhanced_query"] = enhanced_query
        print(f"Enhanced query: {enhanced_query}")
        return state

    def _analyze_query_conditional(self, state: WorkflowState) -> str:
        last_message = state["messages"][-1]
        if isinstance(last_message, dict):
            query = last_message.get('content', '')
        else:
            query = getattr(last_message, 'content', str(last_message))
        ##ask llm if the query is about a chart or data analysis
        prompt = f'''
        You are a data analysis expert. You are given a user query. You need to determine if the query is about a chart or data analysis.
        Assume the user is asking for data unless they specifically ask for a chart/graph/visualization of any kind.
        User query: {query}
        Return only the word "chart" or "data" based on the query.
        '''
        response = client.chat.completions.create(
            model="gpt-4.1",
            messages=[{"role": "user", "content": prompt}]
        )
        result = response.choices[0].message.content
        if "chart" in result.lower():
            return "prepare_graphs"
        else:
            return "prepare_data"
        

    def _prepare_graphs(self, state: WorkflowState) -> WorkflowState:
        print("Preparing graphs")
        query = state["enhanced_query"]
        df = state["df"]
        print(f"Generating chart for query: {query}")
        prompt = f'''
            You are a data analysis expert. You are given a dataset and a user query. You need to generate seaborn python code to create a chart for the user query.
            You can use services like pandas and numpy to manipulate the data as you need. This is encouraged.
            {state["overview"]}
            
            Dataset overview (top five rows): {df.head().to_markdown()}

            Given the dataset above, generate seaborn python code to create a chart for the user query: {query}.

            Be aware, there may be 0 or N/A values in the dataset (especially in the heartrate column).
            Handle these values appropriately.

            Requirements:
            - Use seaborn and matplotlib for visualization
            - Import necessary libraries (seaborn, matplotlib.pyplot, pandas)
            - Refer to the dataset as 'df' in the code
            - Save the chart to 'chart.png' using plt.savefig('chart.png', dpi=300, bbox_inches='tight')
            - Clear the plot after saving using plt.clf()
            - Apply dark theme styling to match the frontend design:
              * Set figure background to black (#000000)
              * Set axes background to dark gray (#111111)
              * Use orange (#FC5200) as the primary accent color for data visualization
              * Use white (#ffffff) for text, titles, and labels
              * Use light gray (#aaaaaa) for secondary text like tick labels
              * Use dark gray (#333333) for grid lines and borders
            - Style the chart with: plt.style.use('dark_background') and customize colors manually
            - Make the chart visually appealing with proper styling that matches a dark theme
            - Include appropriate title, labels, and legend if needed
            - Ensure all text is readable against the dark background
            - IMPORTANT: If file saving fails due to read-only filesystem, the chart will be captured from memory automatically

            RETURN ONLY THE CODE OR ELSE IT WILL FAIL.
        '''
        try:
            response = client.chat.completions.create(
                model="gpt-4.1",
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            code = response.choices[0].message.content
            print(f"Generated chart code: {code}")
            state["chart_code"] = code
            return state
        except Exception as e:
            print(f"Error in generate_chart_code: {e}")
            state["chart_code"] = f"# Error generating chart code: {e}"
            return state

    def _graph_data(self, state: WorkflowState) -> WorkflowState:
        print("Graphing data")
        old_stdout = sys.stdout
        # Redirect standard output to a StringIO object to capture any output generated by the code execution
        sys.stdout = mystdout = StringIO()
        try:
            # Import required libraries
            import seaborn as sns
            import matplotlib.pyplot as plt
            import pandas as pd
            import base64
            import io
            
            # Execute the provided code within the current environment
            code = re.sub(r"^(\s|`)*(?i:python)?\s*", "", state["chart_code"])
            # Removes whitespace & ` from end
            code = re.sub(r"(\s|`)*$", "", code)
            
            # Create namespace with required libraries and data
            namespace = {
                'df': state["df"],
                'sns': sns,
                'plt': plt,
                'pd': pd,
                'base64': base64,
                'io': io
            }
            
            exec(code, namespace)
            
            # Restore the original standard output after code execution
            sys.stdout = old_stdout
            
            # Check if chart was successfully created
            captured_output = mystdout.getvalue()
            print(f"Chart execution output: {captured_output}")
            
            # Try to read the chart file and encode it as base64
            chart_data = None
            try:
                # Check if chart.png exists and read it
                import os
                if os.path.exists("chart.png"):
                    with open("chart.png", "rb") as f:
                        chart_data = base64.b64encode(f.read()).decode('utf-8')
                    print("Chart file found and encoded successfully")
                else:
                    print("Chart file not found")
            except Exception as e:
                print(f"Error reading chart file: {e}")
                # If file system is read-only, try to get the chart from matplotlib's current figure
                try:
                    # Get the current figure and save to bytes
                    fig = plt.gcf()
                    buf = io.BytesIO()
                    fig.savefig(buf, format='png', dpi=300, bbox_inches='tight')
                    buf.seek(0)
                    chart_data = base64.b64encode(buf.read()).decode('utf-8')
                    buf.close()
                    plt.clf()  # Clear the figure
                    print("Chart generated in memory and encoded successfully")
                except Exception as mem_error:
                    print(f"Error generating chart in memory: {mem_error}")
            
            # Set chart output based on success
            if chart_data:
                state["chart_output"] = chart_data
                print("Chart generated and encoded successfully")
            else:
                state["chart_output"] = f"Chart generation failed: {captured_output or 'No output captured'}"
                print(f"Chart generation failed: {captured_output}")
            
            return state
        except Exception as e:
            sys.stdout = old_stdout
            error_msg = f"Error executing chart code: {e}"
            print(error_msg)
            state["chart_output"] = error_msg
            return state

    def _prepare_data(self, state: WorkflowState) -> WorkflowState:
        query = state["enhanced_query"]
        prompt = f'''
            You are a data analysis expert. You are given a dataset and a user query. You need to generate pandas python code to answer the user query. DO NOT GENERATE ANY GRAPHS.
            Ensure you answer the question the user is asking directly. 
            {state["overview"]}

            Given the overview of the dataset above, generate python code to answer the user query: {query}. 

            Refer to the dataset as 'df' in the code.

            Return the id of activities if the user query is about a specific activity.

            Handle 0 values and NaN values appropriately.

            IMPORTANT: Always check if the data exists before using functions like idxmax(), idxmin(), etc. Use .empty or .shape[0] to check if the DataFrame has data.

            Make sure to print the output of the code using 'print(...)'

            Handle edge cases:
            - If no data matches the query, print "No data found"
            - If using idxmax() or idxmin(), check if the DataFrame is not empty first
            - Handle NaN values appropriately

            RETURN ONLY THE CODE OR ELSE IT WILL FAIL. DO NOT GENERATE ANY GRAPHS.
        '''
        try:
            response = client.chat.completions.create(
            model="gpt-4.1",
            messages=[
                {"role": "user", "content": prompt}
            ]
            )
            code = response.choices[0].message.content
            print(code)
            state["code"] = code
            return state
        except Exception as e:
            print(f"Error in generate_code: {e}")
            state["code"] = f"# Error generating code: {e}"
            return state

    def _analyze_data(self, state: WorkflowState) -> WorkflowState:
        old_stdout = sys.stdout
        # Redirect standard output to a StringIO object to capture any output generated by the code execution
        sys.stdout = mystdout = StringIO()
        try:
            # Execute the provided code within the current environment
            code = re.sub(r"^(\s|`)*(?i:python)?\s*", "", state["code"])
            # Removes whitespace & ` from end
            code = re.sub(r"(\s|`)*$", "", code)
            print(code)
            
            # Create namespace with required libraries and data
            namespace = {
                'df': state["df"],
                'pd': pd,
                'numpy': __import__('numpy'),
                'np': __import__('numpy')
            }
            
            exec(code, namespace)
            
            # Restore the original standard output after code execution
            sys.stdout = old_stdout
            
            # Return any captured output from the executed code
            state["output"] = mystdout.getvalue()
            print(state["output"])
            return state
        except Exception as e:
            sys.stdout = old_stdout
            print(f"Error executing code: {e}")
            state["output"] = repr(e)
            return state

    def _verify_graphs(self, state: WorkflowState) -> WorkflowState:
        print("Verifying graphs")
        query = state["enhanced_query"]
        prompt = f'''
        You are a data analysis expert. You are given a dataset and a user query. You need to generate seaborn python code to create a chart for the user query.
        Dataset overview (top five rows): {state["df"].head().to_markdown()}

        User query: {query}.

        Generated code: {state["chart_code"]}

        Please provide feedback on the generated seaborn code, whether the code is valid in syntax and faithful to the user query. If the code appears valid and faithful to the user query, return only the word "valid".
        '''
        response = client.chat.completions.create(
        model="gpt-4.1",
        messages=[
            {"role": "user", "content": prompt}
        ]
        )
        feedback = response.choices[0].message.content

        print(f"Feedback: {feedback}")
        if feedback.lower() == "valid":
            return state
        else:
            prompt = f'''
            You are a data analysis expert. You are given a dataset and a user query. You need to generate seaborn python code to create a chart for the user query.
                {state["overview"]}       

            User query: {query}.

            Generated code: {state["chart_code"]}

            Feedback: {feedback}

            Improve the code with the feedback if only necessary. Otherwise, return the original code.

            Requirements:
            - Use seaborn and matplotlib for visualization
            - Import necessary libraries (seaborn, matplotlib.pyplot, pandas)
            - Refer to the dataset as 'df' in the code
            - Save the chart to 'chart.png' using plt.savefig('chart.png', dpi=300, bbox_inches='tight')
            - Clear the plot after saving using plt.clf()
            - Make the chart visually appealing with proper styling
            - Include appropriate title, labels, and legend if needed

            RETURN ONLY THE CODE OR ELSE IT WILL FAIL.
            '''

            response = client.chat.completions.create(
            model="gpt-4.1",
            messages=[
                {"role": "user", "content": prompt}
            ]
            )
            code = response.choices[0].message.content
            print(code)
            state["chart_code"] = code
            return state


    def _verify_code(self, state: WorkflowState) -> WorkflowState:
        print("Verifying code")
        query = state["enhanced_query"]
        prompt = f'''
        You are a data analysis expert. You are given a dataset and a user query. You need to generate pandas pythoncode to answer the user query.
        Dataset overview (top five rows): {state["df"].head().to_markdown()}

        User query: {query}.

        Generated code: {state["code"]}

        Please provide feedback on the generated code, whether the code is valid in syntax and faithful to the user query. Ensure no graphs/charts are generated. If the code is appears valid and faithful to the user query, return only the word "valid".
        '''
        response = client.chat.completions.create(
        model="gpt-4.1",
        messages=[
            {"role": "user", "content": prompt}
        ]
        )
        feedback = response.choices[0].message.content

        print(f"Feedback: {feedback}")
        if feedback.lower() == "valid":
            return state
        else:
            prompt = f'''
            You are a data analysis expert. You are given a dataset and a user query. You need to generate pandas pythoncode to answer the user query.
                {state["overview"]}       

            User query: {query}.

            Generated code: {state["code"]}

            Feedback: {feedback}

            Improve the code with the feedback if only necessary. Otherwise, return the original code.

            Return only the code without any additional text or formatting.
            Refer the the dataset as 'df' in the code.

            Make sure to print the output of the code using 'print(...)'

            RETURN ONLY THE CODE OR ELSE IT WILL FAIL.
            '''

            response = client.chat.completions.create(
            model="gpt-4.1",
            messages=[
                {"role": "user", "content": prompt}
            ]
            )
            code = response.choices[0].message.content
            print(code)
            state["code"] = code
            return state

    def _final_response(self, state: WorkflowState) -> WorkflowState:
        last_message = state["messages"][-1]
        if isinstance(last_message, dict):
            query = last_message.get('content', '')
        else:
            query = getattr(last_message, 'content', str(last_message))
        prompt = f'''

        Overview: {state["overview"]}

        You are a helpful assistant that generates a response to a user query based on the code output and the chart output.
        Generate a response to the user query based on the code output and the chart output.
        Respond in Markdown format.
        Return only the response, be concise and to the point not conversational.
        If an activity id is returned, include a link to the activity in the response. ex: https://www.strava.com/activities/##IDNUMBER##
        Code output exists: {state["output"] is not None}
        Chart output exists: {state["chart_output"] is not None}
        User query: {query}
        '''
        response = client.chat.completions.create(
            model="gpt-4.1",
            messages=[{"role": "user", "content": prompt}]
        )
        state["response"] = response.choices[0].message.content
        return state

    def run_workflow(self, messages: List[Any], df: pd.DataFrame) -> WorkflowState:
        initial_state = WorkflowState(
            messages=messages,
            df=df,
            chart_code=None,
            chart_output=None,
            overview="""The dataset is a pandas dataframe with the following columns:
            - id: a unique identifier for the activity
            - start_date: the date and time of the activity (NOT a datetime object, just a string)
            - name: the name of the activity
            - distance: the distance of the activity in miles
            - moving_time: the time the activity took to complete in minutes
            - elapsed_time: the total time elapsed in minutes
            - total_elevation_gain: the total elevation gain of the activity in feet
            - start_date_local: the date and time of the activity in the local timezone
            - average_speed: the average speed of the activity in minutes per mile
            - max_speed: the maximum speed of the activity in minutes per mile
            - average_cadence: the average cadence of the activity in steps per minute
            - average_heartrate: the average heartrate of the activity in beats per minute
            - max_heartrate: the maximum heartrate of the activity in beats per minute
            - suffer_score: the suffer score of the activity (a measure of how hard the activity was)
            - year: the year of the activity
            - month: the month of the activity
            - day: the day of the activity
            - day_of_week: the day of the week of the activity
            - time: the time of the activity hh:mm:ss""",
            code=None,
            output=None,
            response=None
        )
        final_state = self.graph.invoke(initial_state)
        
        # Handle the query extraction for the return value
        last_message = messages[-1]
        if isinstance(last_message, dict):
            query = last_message.get('content', '')
        else:
            query = getattr(last_message, 'content', str(last_message))
            
        # Check if chart was actually generated successfully
        # Chart output contains base64 encoded data if successful
        chart_generated = (
            final_state["chart_output"] is not None and 
            not final_state["chart_output"].startswith("Chart generation failed") and
            not final_state["chart_output"].startswith("Error executing chart code")
        )
        
        return {
            "query": query,
            "code_output": final_state["output"],
            "chart_generated": chart_generated,
            "chart_url": f"/chart.png" if chart_generated else None,
            "response": final_state["response"],
            "status": "success"
        }



if __name__ == "__main__":
    #test the graph workflow with fixed_formatted_run_data.csv
    workflow = StravaWorkflow()

    #load the data
    df = pd.read_csv('fixed_formatted_run_data.csv')
    
    while True:
        #run the workflow   
        query = input("Enter a query: ")
        result = workflow.run_workflow([HumanMessage(content=query)], df)
        
    