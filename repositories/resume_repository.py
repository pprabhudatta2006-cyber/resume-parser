from apps.resumes.models import Resume, ParsedResume

class ResumeRepository:
    @staticmethod
    def create_resume(user, file, filename):
        return Resume.objects.create(user=user, file=file, filename=filename)

    @staticmethod
    def get_user_resumes(user):
        return Resume.objects.filter(user=user)

    @staticmethod
    def get_resume_by_id(resume_id, user):
        return Resume.objects.filter(id=resume_id, user=user).first()

    @staticmethod
    def save_parsed_data(resume, data):
        parsed, created = ParsedResume.objects.update_or_create(
            resume=resume,
            defaults=data
        )
        resume.is_parsed = True
        resume.save()
        return parsed
