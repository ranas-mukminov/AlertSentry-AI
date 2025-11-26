from fastapi import APIRouter, HTTPException, BackgroundTasks
from typing import List
from src.models.alert import UnifiedAlert
from src.models.analysis import AnalysisResult
from src.analyzers.classifier import AlertClassifier
from src.responders.slack import SlackResponder
from src.responders.jira import JiraResponder

router = APIRouter()
classifier = AlertClassifier()
slack_responder = SlackResponder()
jira_responder = JiraResponder()

@router.post("/alerts", response_model=AnalysisResult)
async def analyze_alert(alert: UnifiedAlert, background_tasks: BackgroundTasks):
    # Analyze alert
    result = await classifier.analyze(alert)
    if not result:
        raise HTTPException(status_code=500, detail="Analysis failed")

    # Trigger responders in background
    background_tasks.add_task(slack_responder.handle_analysis, result)
    background_tasks.add_task(jira_responder.handle_analysis, result)

    return result

@router.get("/alerts/{alert_id}", response_model=AnalysisResult)
async def get_alert_analysis(alert_id: str):
    # TODO: Implement retrieval from DB
    raise HTTPException(status_code=501, detail="Not implemented")
