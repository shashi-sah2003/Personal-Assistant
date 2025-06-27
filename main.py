import os
import sys
import json
import schedule
import time
from datetime import datetime
from pathlib import Path
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.agents.workflow import run_personal_assistant
from src.api.jira_endpoints import router as jira_router
from src.api.gmail_endpoints import router as gmail_router
from src.api.calendar_endpoints import router as calendar_router
from src.api.slack_endpoints import router as slack_router
from fastapi.responses import JSONResponse
from src.api.unified_endpoints import router as unified_router
import traceback

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


app = FastAPI(
    title="GEP Personal Assistant API",
    description="API for interacting with various workplace services including JIRA, Email, Calendar, and Slack.",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(jira_router)
app.include_router(gmail_router)
app.include_router(calendar_router)
app.include_router(slack_router)
app.include_router(unified_router)


def generate_daily_summary():
    """Generate the daily summary and save it to a file
    """
    print(f"Generating daily summary at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    try:
        result = run_personal_assistant()
        output_dir = Path("output")
        output_dir.mkdir(exist_ok=True)
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")        
        
        json_file = output_dir / f"daily_summary_{timestamp}.json"
        with open(json_file, "w", encoding="utf-8") as f:
            json.dump(result, f, indent=4)
        
        with open(json_file, "r", encoding="utf-8") as f:
            json_content = json.load(f)
        
        return json_content
        
    except Exception as e:
        error_message = f"Error generating daily summary: {str(e)}"
        print(error_message)
        traceback.print_exc()
        
        output_dir = Path("output")
        output_dir.mkdir(exist_ok=True)
        
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        error_file = output_dir / f"error_log_{timestamp}.txt"
        
        with open(error_file, "w", encoding="utf-8") as f:
            f.write(error_message)
            
        return error_message

def schedule_daily_summary(hour=8, minute=30):
    """Schedule the daily summary to run at a specific time
    
    Args:
        hour (int): Hour to run (24-hour format)
        minute (int): Minute to run
    """
    schedule.every().day.at(f"{hour:02d}:{minute:02d}").do(lambda: generate_daily_summary())
    print(f"Daily summary scheduled to run at {hour:02d}:{minute:02d} every day")

@app.get("/run_daily_summary")
async def run_once():
    """Run the daily summary once
    
    """
    result = generate_daily_summary()
    if isinstance(result, dict):
        return JSONResponse(content=result)
    else:
        return JSONResponse(content={"error": result}, status_code=500)

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Personal Assistant")
    parser.add_argument("--schedule", action="store_true", 
                        help="Schedule the daily summary to run at a specific time")
    parser.add_argument("--hour", type=int, default=8,
                        help="Hour to run the scheduled summary (24-hour format)")
    parser.add_argument("--minute", type=int, default=30,
                        help="Minute to run the scheduled summary")
    parser.add_argument("--run-once", action="store_true",
                        help="Run the daily summary once and exit")
    args = parser.parse_args()
    
    if args.run_once:
        print("\n" + "="*80)
        print(f"Starting Personal Assistant - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("="*80 + "\n")
        
        summary = run_once()
        
        print("\n" + "="*80 + "\n")
        print(summary)
        print("\n" + "="*80)
        print("Personal Assistant completed successfully!")
        print("="*80 + "\n")
    elif args.schedule:
        schedule_daily_summary(args.hour, args.minute)
        
        print(f"\n{'='*80}")
        print(f"Personal Assistant Scheduler started at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Next summary will be generated at {args.hour:02d}:{args.minute:02d}")
        print(f"{'='*80}\n")
        print("Press Ctrl+C to stop the scheduler")
        
        try:
            while True:
                schedule.run_pending()
                time.sleep(60) 
        except KeyboardInterrupt:
            print("\nScheduler stopped.")
    else:
        print("\n" + "="*80)
        print("Please specify either --run-once or --schedule")
        print("="*80 + "\n")
        parser.print_help()


