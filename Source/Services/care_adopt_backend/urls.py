from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.utils.safestring import mark_safe
from django.views.generic.base import RedirectView

from rest_framework_extensions.routers import ExtendedDefaultRouter
from rest_framework_swagger.views import get_swagger_view

from apps.landing.views import LandingView
from apps.accounts.views import UserViewSet
from apps.core.api.views import (
    OrganizationViewSet, FacilityViewSet, EmployeeProfileViewSet,
    ProviderTitleViewSet, ProviderRoleViewSet, ProviderSpecialtyViewSet,
    DiagnosisViewSet,  MedicationViewSet, ProcedureViewSet, SymptomViewSet,
    OrganizationEmployeeViewSet, SymptomSearchViewSet, FacilityEmployeeViewSet,
    OrganizationFacilityViewSet, DiagnosisSearchViewSet)
from apps.patients.api.views import (
    PatientProfileViewSet,
    PatientDiagnosisViewSet,
    ProblemAreaViewSet,
    PatientProcedureViewSet,
    PatientMedicationViewSet,
    PatientProfileSearchViewSet,
    PotentialPatientViewSet,
    FacilityInactivePatientViewSet,
)
from apps.plans.api.views import (
    CarePlanTemplateTypeViewSet,
    CarePlanTemplateViewSet,
    CarePlanViewSet,
    PlanConsentViewSet,
    CareTeamMemberViewSet,
    GoalTemplateViewSet,
    GoalViewSet,
    GoalProgressViewSet,
    GoalCommentViewSet,
    InfoMessageQueueViewSet,
    InfoMessageViewSet, )
from apps.tasks.api.views import (
    PatientTaskTemplateViewSet,
    PatientTaskViewSet,
    TeamTaskTemplateViewSet,
    TeamTaskViewSet,
    MedicationTaskTemplateViewSet,
    MedicationTaskViewSet,
    SymptomTaskTemplateViewSet,
    SymptomTaskViewSet,
    SymptomRatingViewSet,
    AssessmentTaskTemplateViewSet,
    AssessmentQuestionViewSet,
    AssessmentTaskViewSet,
    AssessmentResponseViewSet,
    VitalTaskTemplateViewSet,
    VitalTaskViewSet,
    VitalQuestionViewSet,
    VitalResponseViewSet,
    TodaysTasksAPIView,
)
from apps.accounts.views import ObtainAuthToken, \
    RequestPasswordChange, ResetPassword, ValidateUserView

admin.site.site_title = admin.site.index_title = "CareAdopt Backend"
admin.site.site_header = mark_safe('<img src="{img}" alt="{alt}"/> {alt}'.format(
    img=settings.STATIC_URL + 'favicon.ico',
    alt=admin.site.site_title,
))

router = ExtendedDefaultRouter()
# Accounts
router.register(r'users', UserViewSet, base_name='users')
# Core

organization_routes = router.register(
    r'organizations',
    OrganizationViewSet,
    base_name='organizations'
)
organization_routes.register(
    r'employee_profiles',
    OrganizationEmployeeViewSet,
    base_name='organization-employees',
    parents_query_lookups=['organizations']
)
organization_routes.register(
    r'facilities',
    OrganizationFacilityViewSet,
    base_name='organization-facilities',
    parents_query_lookups=['organization']
)

facility_routes = router.register(
    r'facilities',
    FacilityViewSet,
    base_name='facilities'
)
facility_routes.register(
    r'employee_profiles',
    FacilityEmployeeViewSet,
    base_name='facility-employees',
    parents_query_lookups=['facilities']
)
facility_routes.register(
    r'inactive_patients',
    FacilityInactivePatientViewSet,
    base_name='facility-inactive-patients',
    parents_query_lookups=['facility']
)

router.register(
    r'employee_profiles', EmployeeProfileViewSet, base_name='employee_profiles')
router.register(r'provider_titles', ProviderTitleViewSet, base_name='provider_titles')
router.register(r'provider_roles', ProviderRoleViewSet, base_name='provider_roles')
router.register(
    r'provider_specialties', ProviderSpecialtyViewSet, base_name='provider_specialties')
router.register(r'diagnosis', DiagnosisViewSet, base_name='diagnosis')
router.register(
    r'diagnosis/search',
    DiagnosisSearchViewSet,
    base_name="diagnosis-search"
)
router.register(r'medications', MedicationViewSet, base_name='medications')
router.register(r'procedures', ProcedureViewSet, base_name='procedures')
router.register(
    r'symptoms/search',
    SymptomSearchViewSet,
    base_name="symptom-search"
)
router.register(r'symptoms', SymptomViewSet, base_name='symptoms')
# Patients
router.register(
    'patient_profiles/search',
    PatientProfileSearchViewSet,
    base_name='patient_profiles_search',
)
router.register(
    r'patient_profiles', PatientProfileViewSet, base_name='patient_profiles')
router.register(r'problem_areas', ProblemAreaViewSet, base_name='problem_areas')
router.register(
    r'patient_diagnosis', PatientDiagnosisViewSet, base_name='patient_diagnosis')
router.register(
    r'patient_procedures', PatientProcedureViewSet, base_name='patient_procedures')
router.register(
    r'patient_medications', PatientMedicationViewSet, base_name='patient_medications')
# Plans
router.register(
    r'care_plan_template_types',
    CarePlanTemplateTypeViewSet,
    base_name='care_plan_template_types')
router.register(
    r'care_plan_templates', CarePlanTemplateViewSet, base_name='care_plan_templates')
router.register(
    r'care_plans', CarePlanViewSet, base_name='care_plans')
router.register(
    r'plan_consent_forms', PlanConsentViewSet, base_name='plan_consent_forms')
router.register(
    r'care_team_members', CareTeamMemberViewSet, base_name='care_team_members')
router.register(
    r'goal_templates', GoalTemplateViewSet, base_name='goal_templates')
router.register(
    r'goals', GoalViewSet, base_name='goals')
router.register(
    r'goal_progresses', GoalProgressViewSet, base_name='goal_progresses')
router.register(
    r'goal_comments', GoalCommentViewSet, base_name='goal_comments')
router.register(
    r'info_message_queues', InfoMessageQueueViewSet, base_name='info_message_queues')
router.register(
    r'info_messages', InfoMessageViewSet, base_name='info_messages')
router.register(
    r'potential_patients',
    PotentialPatientViewSet,
    base_name='potential_patients')
# Tasks
router.register(
    r'patient_task_templates',
    PatientTaskTemplateViewSet,
    base_name='patient_task_templates')
router.register(r'patient_tasks', PatientTaskViewSet, base_name='patient_tasks')
router.register(
    r'team_task_templates', TeamTaskTemplateViewSet, base_name='team_task_templates')
router.register(
    r'team_tasks', TeamTaskViewSet, base_name='team_tasks')
router.register(
    r'medication_task_templates',
    MedicationTaskTemplateViewSet,
    base_name='medication_task_templates')
router.register(
    r'medication_tasks', MedicationTaskViewSet, base_name='medication_tasks')
router.register(
    r'symptom_task_templates',
    SymptomTaskTemplateViewSet,
    base_name='symptom_task_templates')
router.register(r'symptom_tasks', SymptomTaskViewSet, base_name='symptom_tasks')
router.register(r'symptom_ratings', SymptomRatingViewSet, base_name='symptom_ratings')
router.register(
    r'assessment_task_templates',
    AssessmentTaskTemplateViewSet,
    base_name='assessment_task_templates')
router.register(
    r'assessment_questions',
    AssessmentQuestionViewSet,
    base_name='assessment_questions')
router.register(
    r'assessment_tasks', AssessmentTaskViewSet, base_name='assessment_tasks')
router.register(
    r'assessment_responses',
    AssessmentResponseViewSet,
    base_name='assessment_responses')
router.register(
    r'vital_task_templates',
    VitalTaskTemplateViewSet,
    base_name='vital_task_templates')
router.register(r'vital_tasks', VitalTaskViewSet, base_name='vital_tasks')
router.register(
    r'vital_questions',
    VitalQuestionViewSet,
    base_name='vital_questions')
router.register(
    r'vital_responses',
    VitalResponseViewSet,
    base_name='vital_responses')

schema_view = get_swagger_view(title='CareAdopt API')

urlpatterns = [
    url(r'^favicon.ico$', RedirectView.as_view(
        url=settings.STATIC_URL + 'favicon.ico')),

    url(r'^api/', include('apps.core.api.urls')),
    url(r'^api/', include('apps.patients.api.urls')),
    url(r'^api/', include('apps.plans.api.urls')),

    url(r'^api/', include(router.urls)),
    url(r'^$', LandingView.as_view(), name='landing-page'),

    # Administration
    url(r'^admin/', admin.site.urls),

    # General Api
    url(r'^api-auth/', include('rest_framework.urls',
                               namespace='rest_framework')),
    url(r'^api-token-auth/', ObtainAuthToken.as_view()),
    url(r'reset-password/(?P<email>[a-zA-Z0-9-.+@_]+)/$',
        RequestPasswordChange.as_view(), name='reset-password'),
    url(r'reset/(?P<reset_key>[a-z0-9\-]+)/$',
        ResetPassword.as_view(), name='reset-request'),
    url(r'validate/(?P<validation_key>[a-z0-9\-]+)/$',
        ValidateUserView.as_view(), name='user-validation'),

    # Make sure this comes first before rest-auth URLs
    url(r'^', include('django.contrib.auth.urls')),

    url(r'^rest-auth/', include('rest_auth.urls')),

    url(r'^api/todays_tasks/', TodaysTasksAPIView.as_view(), name="todays_tasks"),
    url(r'^swagger/', schema_view),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
