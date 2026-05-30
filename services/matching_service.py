from typing import List, Dict
from apps.resumes.models import ParsedResume
from apps.matching.models import JobDescription, MatchResult

class MatchingService:
    @staticmethod
    def calculate_match(job: JobDescription, candidate: ParsedResume) -> Dict:
        # Skill Match
        job_skills = set(s.lower() for s in job.required_skills)
        candidate_skills = set(s.lower() for s in candidate.skills)
        
        if not job_skills:
            skill_score = 100.0
        else:
            matches = job_skills.intersection(candidate_skills)
            skill_score = (len(matches) / len(job_skills)) * 100
        
        # Experience Match
        exp_score = 0.0
        if candidate.total_experience_years >= job.min_experience_years:
            exp_score = 100.0
        elif job.min_experience_years > 0:
            exp_score = (candidate.total_experience_years / job.min_experience_years) * 100
            
        # Final Score (Weighted)
        total_score = (skill_score * 0.7) + (exp_score * 0.3)
        
        return {
            'skill_match_score': round(skill_score, 2),
            'experience_match_score': round(exp_score, 2),
            'total_score': round(total_score, 2)
        }
