from accounts.models import ProjectMembership


def refresh_project_memberships(project, new_members):
    members = new_members
    rate = round(100 / len(members))
    ProjectMembership.objects.filter(project=project).delete()
    for m in members:
        ProjectMembership.objects.create(project=project, user=m, rate=rate)
