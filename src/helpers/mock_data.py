
class MockMSGraphData:
    """Mock data provider for Microsoft Graph API"""
    
    @staticmethod
    def get_email_data():
        """Return sample email data"""
        return {
            "value": [
                {
                    "id": "AAMkADE3YmQyZDIwLTZkZjgtNDZjYS05ZjFkLTRhNGRkZGVjMzFiMAAuAAAAAABZIPdvRu-zTJje5FLIVGwmAQDlShgUsTz_SqVJgegVxKjaAAAAAAEMAA==",
                    "subject": "Project Status Update - Urgent Review Needed",
                    "from": "John Smith <john.smith@example.com>",
                    "receivedDateTime": "2025-06-22T08:30:00Z",
                    "bodyPreview": "Hello, We need your urgent review on the project status report attached. There are several critical items that need attention before tomorrow's meeting. Please prioritize this today. Thanks, John"
                },
                {
                    "id": "AAMkADE3YmQyZDIwLTZkZjgtNDZjYS05ZjFkLTRhNGRkZGVjMzFiMAAuAAAAAABZIPdvRu-zTJje5FLIVGwmAQDlShgUsTz_SqVJgegVxKjaAAAAAAEMAB==",
                    "subject": "Quarterly Review Documents",
                    "from": "HR Department <hr@example.com>",
                    "receivedDateTime": "2025-06-21T14:15:00Z",
                    "bodyPreview": "Dear Team Member, Please complete your quarterly review documents by Wednesday. The forms need to be submitted before the end of month for processing. Let me know if you need any assistance."
                },
                {
                    "id": "AAMkADE3YmQyZDIwLTZkZjgtNDZjYS05ZjFkLTRhNGRkZGVjMzFiMAAuAAAAAABZIPdvRu-zTJje5FLIVGwmAQDlShgUsTz_SqVJgegVxKjaAAAAAAEMAC==",
                    "subject": "Team Weekly: Sprint Planning Agenda",
                    "from": "Team Lead <team.lead@example.com>",
                    "receivedDateTime": "2025-06-21T09:45:00Z",
                    "bodyPreview": "Hi team, Here's the agenda for our sprint planning meeting tomorrow. Please review the attached document and come prepared with your task estimates and any blockers you're facing."
                },
                {
                    "id": "AAMkADE3YmQyZDIwLTZkZjgtNDZjYS05ZjFkLTRhNGRkZGVjMzFiMAAuAAAAAABZIPdvRu-zTJje5FLIVGwmAQDlShgUsTz_SqVJgegVxKjaAAAAAAEMAD==",
                    "subject": "Office Building Access Update",
                    "from": "Facilities Management <facilities@example.com>",
                    "receivedDateTime": "2025-06-20T16:30:00Z",
                    "bodyPreview": "Important notice: The building access system will be updated this weekend. Please make sure your access cards are registered with the new system by Friday. There may be brief periods when access is restricted."
                },
                {
                    "id": "AAMkADE3YmQyZDIwLTZkZjgtNDZjYS05ZjFkLTRhNGRkZGVjMzFiMAAuAAAAAABZIPdvRu-zTJje5FLIVGwmAQDlShgUsTz_SqVJgegVxKjaAAAAAAEMAE==",
                    "subject": "Lunch & Learn Session: New Product Features",
                    "from": "Learning & Development <l-and-d@example.com>",
                    "receivedDateTime": "2025-06-20T11:15:00Z",
                    "bodyPreview": "Join us for a Lunch & Learn session next Tuesday at 12:30 PM in Conference Room B. We'll be showcasing the new product features that will be launched next month. Food will be provided!"
                }
            ]
        }
    
    @staticmethod
    def get_calendar_data():
        """Return sample calendar data"""
        return {
            "value": [
                {
                    "id": "AAMkADE3YmQyZDIwLTZkZjgtNDZjYS05ZjFkLTRhNGRkZGVjMzFiMAAuAAAAAABZIPdvRu-zTJje5FLIVGwmAQDlShgUsTz_SqVJgegVxKjaAAAAAAENAAA=",
                    "subject": "Daily Standup",
                    "start": {"dateTime": "2025-06-22T10:00:00", "timeZone": "UTC"},
                    "end": {"dateTime": "2025-06-22T10:15:00", "timeZone": "UTC"},
                    "location": {"displayName": "Teams Meeting"},
                    "organizer": {"emailAddress": {"name": "Team Lead"}},
                    "attendees": [
                        {"emailAddress": {"name": "John Developer"}},
                        {"emailAddress": {"name": "Sarah Designer"}},
                        {"emailAddress": {"name": "Mike Manager"}}
                    ],
                    "bodyPreview": "Daily standup to discuss ongoing tasks and blockers."
                },
                {
                    "id": "AAMkADE3YmQyZDIwLTZkZjgtNDZjYS05ZjFkLTRhNGRkZGVjMzFiMAAuAAAAAABZIPdvRu-zTJje5FLIVGwmAQDlShgUsTz_SqVJgegVxKjaAAAAAAENAAB=",
                    "subject": "Project Review",
                    "start": {"dateTime": "2025-06-22T14:00:00", "timeZone": "UTC"},
                    "end": {"dateTime": "2025-06-22T15:00:00", "timeZone": "UTC"},
                    "location": {"displayName": "Conference Room A"},
                    "organizer": {"emailAddress": {"name": "VP Product"}},
                    "attendees": [
                        {"emailAddress": {"name": "Project Manager"}},
                        {"emailAddress": {"name": "Tech Lead"}},
                        {"emailAddress": {"name": "Design Lead"}}
                    ],
                    "bodyPreview": "Quarterly review of project progress. Please prepare a brief update on your team's progress and any challenges faced."
                },
                {
                    "id": "AAMkADE3YmQyZDIwLTZkZjgtNDZjYS05ZjFkLTRhNGRkZGVjMzFiMAAuAAAAAABZIPdvRu-zTJje5FLIVGwmAQDlShgUsTz_SqVJgegVxKjaAAAAAAENAAC=",
                    "subject": "Sprint Planning",
                    "start": {"dateTime": "2025-06-23T09:00:00", "timeZone": "UTC"},
                    "end": {"dateTime": "2025-06-23T10:30:00", "timeZone": "UTC"},
                    "location": {"displayName": "Teams Meeting"},
                    "organizer": {"emailAddress": {"name": "Scrum Master"}},
                    "attendees": [
                        {"emailAddress": {"name": "Development Team"}},
                        {"emailAddress": {"name": "Product Owner"}},
                        {"emailAddress": {"name": "QA Lead"}}
                    ],
                    "bodyPreview": "Planning session for the next sprint. We'll be discussing the backlog items and estimating tasks."
                }
            ]
        }
    
    @staticmethod
    def get_teams_data():
        """Return sample Teams messages data"""
        return {
            "value": [
                {
                    "id": "1624956089461",
                    "from": {"user": {"displayName": "Project Manager"}},
                    "chatId": "19:d97d6b48-4dac-4569-b212-3e8e37e8f351@thread.v2",
                    "chatName": "Project Alpha Team",
                    "createdDateTime": "2025-06-21T16:45:00Z",
                    "body": {"content": "Can everyone update their tasks in the project board by EOD? We need a current status for tomorrow's review."}
                },
                {
                    "id": "1624956089462",
                    "from": {"user": {"displayName": "Tech Lead"}},
                    "chatId": "19:d97d6b48-4dac-4569-b212-3e8e37e8f351@thread.v2",
                    "chatName": "Project Alpha Team",
                    "createdDateTime": "2025-06-21T16:47:00Z",
                    "body": {"content": "I've identified a potential bottleneck in the API service. @Developer1 and @Developer2, can we meet for 30 minutes tomorrow to discuss solutions?"}
                },
                {
                    "id": "1624956089463",
                    "from": {"user": {"displayName": "HR Manager"}},
                    "chatId": "19:452f7b85-2b93-4589-9932-c8f6f3ae142@thread.v2",
                    "chatName": "HR Direct Chat",
                    "createdDateTime": "2025-06-21T14:30:00Z",
                    "body": {"content": "Just a reminder that you need to complete the quarterly review form by Wednesday. Let me know if you need any help with it."}
                },
                {
                    "id": "1624956089464",
                    "from": {"user": {"displayName": "Marketing Director"}},
                    "chatId": "19:a92b5447-1d57-4837-bc41-92d22f9039@thread.v2",
                    "chatName": "Cross-department Collaboration",
                    "createdDateTime": "2025-06-21T11:15:00Z",
                    "body": {"content": "We need technical input for the upcoming product launch. @You Can you help us prepare some technical specifications that marketing can understand? I'd need this by Thursday."}
                }
            ]
        }

class MockJiraData:
    """Mock data provider for JIRA API"""
    
    @staticmethod
    def get_mock_issues():
        """Return sample JIRA issues"""
        from types import SimpleNamespace
        
        issues = []
        
        issue1 = SimpleNamespace()
        issue1.key = "PROJ-123"
        issue1.fields = SimpleNamespace()
        issue1.fields.summary = "Fix critical authentication bug in login flow"
        issue1.fields.status = SimpleNamespace(name="In Progress")
        issue1.fields.priority = SimpleNamespace(name="High")
        issue1.fields.assignee = SimpleNamespace(displayName="Current User")
        issue1.fields.duedate = "2025-06-24"
        issue1.fields.description = "Users are experiencing intermittent login failures. This needs immediate attention."
        issues.append(issue1)
        
        issue2 = SimpleNamespace()
        issue2.key = "PROJ-456"
        issue2.fields = SimpleNamespace()
        issue2.fields.summary = "Implement new dashboard feature"
        issue2.fields.status = SimpleNamespace(name="To Do")
        issue2.fields.priority = SimpleNamespace(name="Medium")
        issue2.fields.assignee = SimpleNamespace(displayName="Current User")
        issue2.fields.duedate = "2025-06-30"
        issue2.fields.description = "Create a new dashboard that shows user analytics based on the requirements document."
        issues.append(issue2)
        
        issue3 = SimpleNamespace()
        issue3.key = "PROJ-789"
        issue3.fields = SimpleNamespace()
        issue3.fields.summary = "Update documentation for API endpoints"
        issue3.fields.status = SimpleNamespace(name="To Do")
        issue3.fields.priority = SimpleNamespace(name="Low")
        issue3.fields.assignee = SimpleNamespace(displayName="Current User")
        issue3.fields.duedate = "2025-07-15"
        issue3.fields.description = "The API documentation needs to be updated to reflect recent changes."
        issues.append(issue3)
        
        issue4 = SimpleNamespace()
        issue4.key = "PROJ-234"
        issue4.fields = SimpleNamespace()
        issue4.fields.summary = "Research cloud migration options"
        issue4.fields.status = SimpleNamespace(name="In Progress")
        issue4.fields.priority = SimpleNamespace(name="Medium")
        issue4.fields.assignee = SimpleNamespace(displayName="Another Developer")
        issue4.fields.duedate = "2025-07-01"
        issue4.fields.description = "Evaluate different cloud providers for our application migration."
        issues.append(issue4)
        
        return issues
