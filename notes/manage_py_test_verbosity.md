
- Search this file for 'skip` to see if there are any tests that are skipped due to missing templates or other issues.

```bash
(personal-assistant) flynntknapp@DELL-DESK:~/Programming/personal-assistant$ python manage.py test --verbosity=2 app_tracker
Found 204 test(s).
Creating test database for alias 'default' ('file:memorydb_default?mode=memory&cache=shared')...
Operations to perform:
  Synchronize unmigrated apps: admindocs, messages, rest_framework, staticfiles, storages
  Apply all migrations: accounts, activity_tracker, admin, app_tracker, auth, boosts, care_craft, career_organizerator, cbt, contenttypes, django_celery_beat, do_it, goals, journal, opportunity_search, pharma_tracker, pi_tracker, plan_it, self_enquiry, sessions, sonic_text, storager, story_line, uc_goals, unimportant_notes, value_centric, vitals
Synchronizing apps without migrations:
  Creating tables...
    Running deferred SQL...
Running migrations:
  Applying contenttypes.0001_initial... OK
  Applying contenttypes.0002_remove_content_type_name... OK
  Applying auth.0001_initial... OK
  Applying auth.0002_alter_permission_name_max_length... OK
  Applying auth.0003_alter_user_email_max_length... OK
  Applying auth.0004_alter_user_username_opts... OK
  Applying auth.0005_alter_user_last_login_null... OK
  Applying auth.0006_require_contenttypes_0002... OK
  Applying auth.0007_alter_validators_add_error_messages... OK
  Applying auth.0008_alter_user_username_max_length... OK
  Applying auth.0009_alter_user_last_name_max_length... OK
  Applying auth.0010_alter_group_name_max_length... OK
  Applying auth.0011_update_proxy_permissions... OK
  Applying auth.0012_alter_user_first_name_max_length... OK
  Applying accounts.0001_initial... OK
  Applying accounts.0002_customuser_registration_accepted... OK
  Applying accounts.0003_alter_customuser_registration_accepted... OK
  Applying accounts.0004_customuser_beastie... OK
  Applying activity_tracker.0001_initial... OK
  Applying activity_tracker.0002_alter_activity_notes_alter_activitycompleted_date... OK
  Applying activity_tracker.0003_alter_activitycompleted_activity... OK
  Applying activity_tracker.0004_alter_activitycompleted_date... OK
  Applying admin.0001_initial... OK
  Applying admin.0002_logentry_remove_auto_add... OK
  Applying admin.0003_logentry_add_action_flag_choices... OK
  Applying app_tracker.0001_initial... OK
  Applying app_tracker.0002_alter_application_language_framework_systems_and_more... OK
  Applying app_tracker.0003_alter_application_has_custom_user... OK
  Applying app_tracker.0004_alter_application_has_prod_deployment_and_more... OK
  Applying app_tracker.0005_alter_application_repository_url_and_more... OK
  Applying app_tracker.0006_alter_note_application... OK
  Applying app_tracker.0007_application_has_email_sending_and_more... OK
  Applying app_tracker.0008_application_repository_is_public_and_more... OK
  Applying app_tracker.0009_application_production_url... OK
  Applying app_tracker.0010_application_project_board_url... OK
  Applying app_tracker.0011_application_is_template_repository_and_more... OK
  Applying app_tracker.0012_application_settings_in_dot_env_file... OK
  Applying app_tracker.0013_application_settings_in_dot_yml_file... OK
  Applying app_tracker.0014_application_is_favorite... OK
  Applying app_tracker.0015_application_settings_in_environment... OK
  Applying app_tracker.0016_application_reference_repository_url... OK
  Applying app_tracker.0017_project_application_project... OK
  Applying app_tracker.0018_alter_project_owner... OK
  Applying app_tracker.0019_application_is_official_repository... OK
  Applying app_tracker.0020_application_is_archive_repository_and_more... OK
  Applying app_tracker.0021_organizationalconcept... OK
  Applying app_tracker.0022_organizationalconcept_applications... OK
  Applying app_tracker.0023_alter_organizationalconcept_applications... OK
  Applying app_tracker.0024_application_has_cicd... OK
  Applying app_tracker.0025_alter_application_has_cicd... OK
  Applying app_tracker.0026_application_is_simple_example... OK
  Applying app_tracker.0027_label... OK
  Applying app_tracker.0028_alter_label_application... OK
  Applying app_tracker.0029_application_all_tests_passing... OK
  Applying app_tracker.0030_application_is_adapted_repository... OK
  Applying app_tracker.0031_application_reference_url... OK
  Applying app_tracker.0032_operatingsystem_server... OK
  Applying app_tracker.0033_alter_operatingsystem_options... OK
  Applying boosts.0001_initial... OK
  Applying boosts.0002_rename_statement_statement_body... OK
  Applying boosts.0003_alter_statement_date_created... OK
  Applying boosts.0004_rename_date_created_statement_created... OK
  Applying boosts.0005_alter_statement_author... OK
  Applying boosts.0006_rename_statement_inspirational... OK
  Applying boosts.0007_alter_inspirational_author... OK
  Applying boosts.0008_alter_inspirational_body... OK
  Applying boosts.0009_alter_inspirational_body... OK
  Applying boosts.0010_inspirationsent... OK
  Applying boosts.0011_inspirationsent_inspirational_text... OK
  Applying boosts.0012_alter_inspirationsent_options... OK
  Applying boosts.0013_rename_inspirationsent_inspirationalsent... OK
  Applying boosts.0014_alter_inspirationalsent_sender... OK
  Applying care_craft.0001_initial... OK
  Applying care_craft.0002_alter_activity_options... OK
  Applying care_craft.0003_carecraftnote... OK
  Applying career_organizerator.0001_initial... OK
  Applying career_organizerator.0002_skill... OK
  Applying career_organizerator.0003_behavioralinterviewquestion... OK
  Applying career_organizerator.0004_questionresponse... OK
  Applying career_organizerator.0005_alter_questionresponse_text... OK
  Applying career_organizerator.0006_alter_behavioralinterviewquestion_text_and_more... OK
  Applying career_organizerator.0007_purpose... OK
  Applying career_organizerator.0008_questionresponse_summary... OK
  Applying career_organizerator.0009_skill_order... OK
  Applying cbt.0001_initial... OK
  Applying cbt.0002_thought... OK
  Applying cbt.0003_thought_cognative_distortion... OK
  Applying cbt.0004_alter_thought_cognative_distortion... OK
  Applying cbt.0005_remove_thought_cognative_distortion_and_more... OK
  Applying cbt.0006_rename_cognativedistortion_cognitivedistortion... OK
  Applying cbt.0007_remove_thought_cognative_distortion_and_more... OK
  Applying cbt.0008_alter_thought_cognitive_distortion... OK
  Applying django_celery_beat.0001_initial... OK
  Applying django_celery_beat.0002_auto_20161118_0346... OK
  Applying django_celery_beat.0003_auto_20161209_0049... OK
  Applying django_celery_beat.0004_auto_20170221_0000... OK
  Applying django_celery_beat.0005_add_solarschedule_events_choices... OK
  Applying django_celery_beat.0006_auto_20180322_0932... OK
  Applying django_celery_beat.0007_auto_20180521_0826... OK
  Applying django_celery_beat.0008_auto_20180914_1922... OK
  Applying django_celery_beat.0006_auto_20180210_1226... OK
  Applying django_celery_beat.0006_periodictask_priority... OK
  Applying django_celery_beat.0009_periodictask_headers... OK
  Applying django_celery_beat.0010_auto_20190429_0326... OK
  Applying django_celery_beat.0011_auto_20190508_0153... OK
  Applying django_celery_beat.0012_periodictask_expire_seconds... OK
  Applying django_celery_beat.0013_auto_20200609_0727... OK
  Applying django_celery_beat.0014_remove_clockedschedule_enabled... OK
  Applying django_celery_beat.0015_edit_solarschedule_events_choices... OK
  Applying django_celery_beat.0016_alter_crontabschedule_timezone... OK
  Applying django_celery_beat.0017_alter_crontabschedule_month_of_year... OK
  Applying django_celery_beat.0018_improve_crontab_helptext... OK
  Applying django_celery_beat.0019_alter_periodictasks_options... OK
  Applying do_it.0001_initial... OK
  Applying goals.0001_initial... OK
  Applying goals.0002_alter_goalrelationship_options_and_more... OK
  Applying goals.0002_alter_goal_options_alter_goalrelationship_options... OK
  Applying goals.0003_merge_20241225_1845... OK
  Applying journal.0001_initial... OK
  Applying journal.0002_alter_entry_options... OK
  Applying opportunity_search.0001_initial... OK
  Applying opportunity_search.0002_alter_worksearchactivity_options... OK
  Applying pharma_tracker.0001_initial... OK
  Applying pi_tracker.0001_initial... OK
  Applying pi_tracker.0002_alter_pidevice_mac_address_alter_pidevice_ram... OK
  Applying plan_it.0001_initial... OK
  Applying plan_it.0002_alter_activity_options_and_more... OK
  Applying plan_it.0003_activitylocation_parent_location... OK
  Applying plan_it.0004_activityinstance... OK
  Applying plan_it.0005_alter_activityinstance_options... OK
  Applying self_enquiry.0001_initial... OK
  Applying self_enquiry.0002_journal_updated_alter_journal_created... OK
  Applying self_enquiry.0003_growthopportunity... OK
  Applying self_enquiry.0004_alter_growthopportunity_options_and_more... OK
  Applying self_enquiry.0005_alter_growthopportunity_created... OK
  Applying self_enquiry.0006_alter_growthopportunity_created_and_more... OK
  Applying self_enquiry.0007_alter_journal_created... OK
  Applying self_enquiry.0008_alter_growthopportunity_created_and_more... OK
  Applying sessions.0001_initial... OK
  Applying sonic_text.0001_initial... OK
  Applying storager.0001_initial... OK
  Applying story_line.0001_initial... OK
  Applying uc_goals.0001_initial... OK
  Applying uc_goals.0002_goal_is_archived... OK
  Applying uc_goals.0003_virtue_viacharacterstrength... OK
  Applying uc_goals.0004_goal_character_strengths... OK
  Applying unimportant_notes.0001_initial... OK
  Applying unimportant_notes.0002_rename_note_unimportantnote... OK
  Applying unimportant_notes.0003_alter_unimportantnote_options... OK
  Applying unimportant_notes.0004_unimportantnote_url_alter_unimportantnote_content... OK
  Applying unimportant_notes.0005_unimportantnote_main_image... OK
  Applying unimportant_notes.0006_alter_unimportantnote_main_image... OK
  Applying unimportant_notes.0007_notetag_unimportantnote_tag... OK
  Applying unimportant_notes.0008_notetag_author... OK
  Applying value_centric.0001_initial... OK
  Applying vitals.0001_initial... OK
  Applying vitals.0002_pulse... OK
  Applying vitals.0003_alter_bloodpressure_options... OK
  Applying vitals.0004_alter_bloodpressure_diastolic_and_more... OK
  Applying vitals.0005_bloodpressure_pulse... OK
  Applying vitals.0006_temperature... OK
  Applying vitals.0007_bodyweight... OK
System check identified no issues (0 silenced).
test_fieldsets (app_tracker.tests.test_admin.ApplicationAdminTest.test_fieldsets) ... ok
test_language_framework_systems_list_method (app_tracker.tests.test_admin.ApplicationAdminTest.test_language_framework_systems_list_method)
Tests for the 'language_framework_systems_list' method using real ... ok
test_language_framework_systems_list_method_mock (app_tracker.tests.test_admin.ApplicationAdminTest.test_language_framework_systems_list_method_mock)
Tests for the 'language_framework_systems_list' method using a mock. ... ok
test_list_display (app_tracker.tests.test_admin.ApplicationAdminTest.test_list_display) ... ok
test_list_filter (app_tracker.tests.test_admin.ApplicationAdminTest.test_list_filter) ... ok
test_ordering (app_tracker.tests.test_admin.ApplicationAdminTest.test_ordering) ... ok
test_readonly_fields (app_tracker.tests.test_admin.ApplicationAdminTest.test_readonly_fields) ... ok
test_search_fields (app_tracker.tests.test_admin.ApplicationAdminTest.test_search_fields) ... ok
test_fieldsets (app_tracker.tests.test_admin.LabelAdminTest.test_fieldsets) ... ok
test_list_display (app_tracker.tests.test_admin.LabelAdminTest.test_list_display) ... ok
test_list_filter (app_tracker.tests.test_admin.LabelAdminTest.test_list_filter) ... ok
test_ordering (app_tracker.tests.test_admin.LabelAdminTest.test_ordering) ... ok
test_readonly_fields (app_tracker.tests.test_admin.LabelAdminTest.test_readonly_fields) ... ok
test_search_fields (app_tracker.tests.test_admin.LabelAdminTest.test_search_fields) ... ok
test_fieldsets (app_tracker.tests.test_admin.LanguageFrameworkSystemAdminTest.test_fieldsets) ... ok
test_list_display (app_tracker.tests.test_admin.LanguageFrameworkSystemAdminTest.test_list_display) ... ok
test_list_filter (app_tracker.tests.test_admin.LanguageFrameworkSystemAdminTest.test_list_filter) ... ok
test_ordering (app_tracker.tests.test_admin.LanguageFrameworkSystemAdminTest.test_ordering) ... ok
test_readonly_fields (app_tracker.tests.test_admin.LanguageFrameworkSystemAdminTest.test_readonly_fields) ... ok
test_search_fields (app_tracker.tests.test_admin.LanguageFrameworkSystemAdminTest.test_search_fields) ... ok
test_applications_list (app_tracker.tests.test_admin.OrganizationalConceptAdminTest.test_applications_list)
Tests for the 'applications_list' method using real objects. ... ok
test_applications_list_mock (app_tracker.tests.test_admin.OrganizationalConceptAdminTest.test_applications_list_mock)
Tests for the 'applications_list' method using a mock. ... ok
test_fieldsets (app_tracker.tests.test_admin.OrganizationalConceptAdminTest.test_fieldsets) ... ok
test_list_display (app_tracker.tests.test_admin.OrganizationalConceptAdminTest.test_list_display) ... ok
test_list_filter (app_tracker.tests.test_admin.OrganizationalConceptAdminTest.test_list_filter) ... ok
test_ordering (app_tracker.tests.test_admin.OrganizationalConceptAdminTest.test_ordering) ... ok
test_readonly_fields (app_tracker.tests.test_admin.OrganizationalConceptAdminTest.test_readonly_fields) ... ok
test_search_fields (app_tracker.tests.test_admin.OrganizationalConceptAdminTest.test_search_fields) ... ok
test_application_list_method (app_tracker.tests.test_admin.ProjectAdminTest.test_application_list_method)
Tests for the 'application_list' method using real objects. ... ok
test_application_list_method_mock (app_tracker.tests.test_admin.ProjectAdminTest.test_application_list_method_mock)
Tests for the 'application_list' method using a mock. ... ok
test_fieldsets (app_tracker.tests.test_admin.ProjectAdminTest.test_fieldsets) ... ok
test_list_display (app_tracker.tests.test_admin.ProjectAdminTest.test_list_display) ... ok
test_list_filter (app_tracker.tests.test_admin.ProjectAdminTest.test_list_filter) ... ok
test_ordering (app_tracker.tests.test_admin.ProjectAdminTest.test_ordering) ... ok
test_owner_list_method (app_tracker.tests.test_admin.ProjectAdminTest.test_owner_list_method)
Tests for the 'owner_list' method using real objects. ... ok
test_readonly_fields (app_tracker.tests.test_admin.ProjectAdminTest.test_readonly_fields) ... ok
test_search_fields (app_tracker.tests.test_admin.ProjectAdminTest.test_search_fields) ... ok
test_application_str_and_get_absolute_url_and_m2m (app_tracker.tests.test_full_coverage.ModelTestCase.test_application_str_and_get_absolute_url_and_m2m) ... ok
test_django_model_str_and_foreignkey (app_tracker.tests.test_full_coverage.ModelTestCase.test_django_model_str_and_foreignkey) ... ok
test_label_str_and_m2m (app_tracker.tests.test_full_coverage.ModelTestCase.test_label_str_and_m2m) ... ok
test_language_framework_system_str (app_tracker.tests.test_full_coverage.ModelTestCase.test_language_framework_system_str) ... ok
test_note_str_with_and_without_application (app_tracker.tests.test_full_coverage.ModelTestCase.test_note_str_with_and_without_application) ... ok
test_operating_system_str (app_tracker.tests.test_full_coverage.ModelTestCase.test_operating_system_str) ... ok
test_organizational_concept_str_and_app_count (app_tracker.tests.test_full_coverage.ModelTestCase.test_organizational_concept_str_and_app_count) ... ok
test_project_str_and_owner_m2m (app_tracker.tests.test_full_coverage.ModelTestCase.test_project_str_and_owner_m2m) ... ok
test_server_str_and_fields (app_tracker.tests.test_full_coverage.ModelTestCase.test_server_str_and_fields) ... ok
test_reverse_detail_update_delete_urls (app_tracker.tests.test_full_coverage.URLTests.test_reverse_detail_update_delete_urls) ... ok
test_reverse_list_and_create_urls (app_tracker.tests.test_full_coverage.URLTests.test_reverse_list_and_create_urls) ... ok
test_application_crud (app_tracker.tests.test_full_coverage.ViewTestCase.test_application_crud) ... ok
test_home_view_render (app_tracker.tests.test_full_coverage.ViewTestCase.test_home_view_render)
The home() view should return 200 and contain "App Tracker Home" in the HTML. ... ok
test_label_crud (app_tracker.tests.test_full_coverage.ViewTestCase.test_label_crud) ... ok
test_lfs_crud (app_tracker.tests.test_full_coverage.ViewTestCase.test_lfs_crud) ... ok
test_note_crud (app_tracker.tests.test_full_coverage.ViewTestCase.test_note_crud) ... ok
test_operating_system_crud (app_tracker.tests.test_full_coverage.ViewTestCase.test_operating_system_crud) ... ok
test_organizational_concept_crud (app_tracker.tests.test_full_coverage.ViewTestCase.test_organizational_concept_crud) ... skipped 'Missing template for oc_detail'
test_project_crud (app_tracker.tests.test_full_coverage.ViewTestCase.test_project_crud) ... ok
test_server_crud (app_tracker.tests.test_full_coverage.ViewTestCase.test_server_crud) ... ok
test_all_tests_passing_default_false (app_tracker.tests.test_models.ApplicationModelTest.test_all_tests_passing_default_false) ... ok
test_all_tests_passing_help_text (app_tracker.tests.test_models.ApplicationModelTest.test_all_tests_passing_help_text) ... ok
test_all_tests_passing_verbose_name (app_tracker.tests.test_models.ApplicationModelTest.test_all_tests_passing_verbose_name) ... ok
test_description_blank_true (app_tracker.tests.test_models.ApplicationModelTest.test_description_blank_true) ... ok
test_description_help_text (app_tracker.tests.test_models.ApplicationModelTest.test_description_help_text) ... ok
test_description_null_true (app_tracker.tests.test_models.ApplicationModelTest.test_description_null_true) ... ok
test_description_verbose_name (app_tracker.tests.test_models.ApplicationModelTest.test_description_verbose_name) ... ok
test_has_cicd_default_false (app_tracker.tests.test_models.ApplicationModelTest.test_has_cicd_default_false) ... ok
test_has_cicd_help_text (app_tracker.tests.test_models.ApplicationModelTest.test_has_cicd_help_text) ... ok
test_has_cicd_verbose_name (app_tracker.tests.test_models.ApplicationModelTest.test_has_cicd_verbose_name) ... ok
test_has_custom_user_default_false (app_tracker.tests.test_models.ApplicationModelTest.test_has_custom_user_default_false) ... ok
test_has_custom_user_help_text (app_tracker.tests.test_models.ApplicationModelTest.test_has_custom_user_help_text) ... ok
test_has_custom_user_verbose_name (app_tracker.tests.test_models.ApplicationModelTest.test_has_custom_user_verbose_name) ... ok
test_has_email_sending_default_false (app_tracker.tests.test_models.ApplicationModelTest.test_has_email_sending_default_false) ... ok
test_has_email_sending_help_text (app_tracker.tests.test_models.ApplicationModelTest.test_has_email_sending_help_text) ... ok
test_has_email_sending_verbose_name (app_tracker.tests.test_models.ApplicationModelTest.test_has_email_sending_verbose_name) ... ok
test_has_prod_deployment_default_false (app_tracker.tests.test_models.ApplicationModelTest.test_has_prod_deployment_default_false) ... ok
test_has_prod_deployment_help_text (app_tracker.tests.test_models.ApplicationModelTest.test_has_prod_deployment_help_text) ... ok
test_has_prod_deployment_verbose_name (app_tracker.tests.test_models.ApplicationModelTest.test_has_prod_deployment_verbose_name) ... ok
test_has_sticky_footer_default_false (app_tracker.tests.test_models.ApplicationModelTest.test_has_sticky_footer_default_false) ... ok
test_has_sticky_footer_help_text (app_tracker.tests.test_models.ApplicationModelTest.test_has_sticky_footer_help_text) ... ok
test_has_sticky_footer_verbose_name (app_tracker.tests.test_models.ApplicationModelTest.test_has_sticky_footer_verbose_name) ... ok
test_is_adapted_repository (app_tracker.tests.test_models.ApplicationModelTest.test_is_adapted_repository) ... ok
test_is_archive_repository_default_false (app_tracker.tests.test_models.ApplicationModelTest.test_is_archive_repository_default_false) ... ok
test_is_archive_repository_help_text (app_tracker.tests.test_models.ApplicationModelTest.test_is_archive_repository_help_text) ... ok
test_is_archive_repository_verbose_name (app_tracker.tests.test_models.ApplicationModelTest.test_is_archive_repository_verbose_name) ... ok
test_is_favorite_default_false (app_tracker.tests.test_models.ApplicationModelTest.test_is_favorite_default_false) ... ok
test_is_favorite_help_text (app_tracker.tests.test_models.ApplicationModelTest.test_is_favorite_help_text) ... ok
test_is_favorite_verbose_name (app_tracker.tests.test_models.ApplicationModelTest.test_is_favorite_verbose_name) ... ok
test_is_official_repository_default_false (app_tracker.tests.test_models.ApplicationModelTest.test_is_official_repository_default_false) ... ok
test_is_official_repository_help_text (app_tracker.tests.test_models.ApplicationModelTest.test_is_official_repository_help_text) ... ok
test_is_official_repository_verbose_name (app_tracker.tests.test_models.ApplicationModelTest.test_is_official_repository_verbose_name) ... ok
test_is_simple_example_default_false (app_tracker.tests.test_models.ApplicationModelTest.test_is_simple_example_default_false) ... ok
test_is_simple_example_help_text (app_tracker.tests.test_models.ApplicationModelTest.test_is_simple_example_help_text) ... ok
test_is_simple_example_verbose_name (app_tracker.tests.test_models.ApplicationModelTest.test_is_simple_example_verbose_name) ... ok
test_is_template_repository_default_false (app_tracker.tests.test_models.ApplicationModelTest.test_is_template_repository_default_false) ... ok
test_is_template_repository_help_text (app_tracker.tests.test_models.ApplicationModelTest.test_is_template_repository_help_text) ... ok
test_is_template_repository_verbose_name (app_tracker.tests.test_models.ApplicationModelTest.test_is_template_repository_verbose_name) ... ok
test_language_framework_systems_dunder_string_method (app_tracker.tests.test_models.ApplicationModelTest.test_language_framework_systems_dunder_string_method) ... ok
test_language_framework_systems_help_text (app_tracker.tests.test_models.ApplicationModelTest.test_language_framework_systems_help_text) ... ok
test_language_framework_systems_related_name (app_tracker.tests.test_models.ApplicationModelTest.test_language_framework_systems_related_name) ... ok
test_language_framework_systems_uses_proper_model (app_tracker.tests.test_models.ApplicationModelTest.test_language_framework_systems_uses_proper_model) ... ok
test_language_framework_systems_verbose_name (app_tracker.tests.test_models.ApplicationModelTest.test_language_framework_systems_verbose_name) ... ok
test_name_help_text (app_tracker.tests.test_models.ApplicationModelTest.test_name_help_text) ... ok
test_name_max_length (app_tracker.tests.test_models.ApplicationModelTest.test_name_max_length) ... ok
test_name_unique_true (app_tracker.tests.test_models.ApplicationModelTest.test_name_unique_true) ... ok
test_name_verbose_name (app_tracker.tests.test_models.ApplicationModelTest.test_name_verbose_name) ... ok
test_production_url_blank_true (app_tracker.tests.test_models.ApplicationModelTest.test_production_url_blank_true) ... ok
test_production_url_help_text (app_tracker.tests.test_models.ApplicationModelTest.test_production_url_help_text) ... ok
test_production_url_null_true (app_tracker.tests.test_models.ApplicationModelTest.test_production_url_null_true) ... ok
test_production_url_verbose_name (app_tracker.tests.test_models.ApplicationModelTest.test_production_url_verbose_name) ... ok
test_project_blank_true (app_tracker.tests.test_models.ApplicationModelTest.test_project_blank_true) ... ok
test_project_board_url_blank_true (app_tracker.tests.test_models.ApplicationModelTest.test_project_board_url_blank_true) ... ok
test_project_board_url_help_text (app_tracker.tests.test_models.ApplicationModelTest.test_project_board_url_help_text) ... ok
test_project_board_url_null_true (app_tracker.tests.test_models.ApplicationModelTest.test_project_board_url_null_true) ... ok
test_project_board_url_verbose_name (app_tracker.tests.test_models.ApplicationModelTest.test_project_board_url_verbose_name) ... ok
test_project_help_text (app_tracker.tests.test_models.ApplicationModelTest.test_project_help_text) ... ok
test_project_related_name (app_tracker.tests.test_models.ApplicationModelTest.test_project_related_name) ... ok
test_project_verbose_name (app_tracker.tests.test_models.ApplicationModelTest.test_project_verbose_name) ... ok
test_reference_repository_url_help_text (app_tracker.tests.test_models.ApplicationModelTest.test_reference_repository_url_help_text) ... ok
test_reference_repository_url_verbose_name (app_tracker.tests.test_models.ApplicationModelTest.test_reference_repository_url_verbose_name) ... ok
test_reference_url_field (app_tracker.tests.test_models.ApplicationModelTest.test_reference_url_field)
`reference_url` should have the following attributes and values: ... ok
test_repository_is_public_default_false (app_tracker.tests.test_models.ApplicationModelTest.test_repository_is_public_default_false) ... ok
test_repository_is_public_help_text (app_tracker.tests.test_models.ApplicationModelTest.test_repository_is_public_help_text) ... ok
test_repository_is_public_verbose_name (app_tracker.tests.test_models.ApplicationModelTest.test_repository_is_public_verbose_name) ... ok
test_repository_url_blank_true (app_tracker.tests.test_models.ApplicationModelTest.test_repository_url_blank_true) ... ok
test_repository_url_help_text (app_tracker.tests.test_models.ApplicationModelTest.test_repository_url_help_text) ... ok
test_repository_url_null_true (app_tracker.tests.test_models.ApplicationModelTest.test_repository_url_null_true) ... ok
test_repository_url_verbose_name (app_tracker.tests.test_models.ApplicationModelTest.test_repository_url_verbose_name) ... ok
test_settings_in_dot_env_file_default_false (app_tracker.tests.test_models.ApplicationModelTest.test_settings_in_dot_env_file_default_false) ... ok
test_settings_in_dot_env_file_help_text (app_tracker.tests.test_models.ApplicationModelTest.test_settings_in_dot_env_file_help_text) ... ok
test_settings_in_dot_env_file_verbose_name (app_tracker.tests.test_models.ApplicationModelTest.test_settings_in_dot_env_file_verbose_name) ... ok
test_settings_in_dot_yml_file_default_false (app_tracker.tests.test_models.ApplicationModelTest.test_settings_in_dot_yml_file_default_false) ... ok
test_settings_in_dot_yml_file_help_text (app_tracker.tests.test_models.ApplicationModelTest.test_settings_in_dot_yml_file_help_text) ... ok
test_settings_in_dot_yml_file_verbose_name (app_tracker.tests.test_models.ApplicationModelTest.test_settings_in_dot_yml_file_verbose_name) ... ok
test_settings_in_environment_default_false (app_tracker.tests.test_models.ApplicationModelTest.test_settings_in_environment_default_false) ... ok
test_settings_in_environment_help_text (app_tracker.tests.test_models.ApplicationModelTest.test_settings_in_environment_help_text) ... ok
test_settings_in_environment_verbose_name (app_tracker.tests.test_models.ApplicationModelTest.test_settings_in_environment_verbose_name) ... ok
test_testing_level_blank_true (app_tracker.tests.test_models.ApplicationModelTest.test_testing_level_blank_true) ... ok
test_testing_level_choices_has_correct_choices (app_tracker.tests.test_models.ApplicationModelTest.test_testing_level_choices_has_correct_choices) ... ok
test_testing_level_choices_has_four_choices (app_tracker.tests.test_models.ApplicationModelTest.test_testing_level_choices_has_four_choices) ... ok
test_testing_level_help_text (app_tracker.tests.test_models.ApplicationModelTest.test_testing_level_help_text) ... ok
test_testing_level_max_length (app_tracker.tests.test_models.ApplicationModelTest.test_testing_level_max_length) ... ok
test_testing_level_null_true (app_tracker.tests.test_models.ApplicationModelTest.test_testing_level_null_true) ... ok
test_testing_level_verbose_name (app_tracker.tests.test_models.ApplicationModelTest.test_testing_level_verbose_name) ... ok
test_application_on_delete_cascade (app_tracker.tests.test_models.DjangoModelModelTest.test_application_on_delete_cascade) ... ok
test_application_related_name (app_tracker.tests.test_models.DjangoModelModelTest.test_application_related_name)
This tests the related_name of the application field. Though we are ... ok
test_application_verbose_name (app_tracker.tests.test_models.DjangoModelModelTest.test_application_verbose_name) ... ok
test_description_help_text (app_tracker.tests.test_models.DjangoModelModelTest.test_description_help_text) ... ok
test_description_verbose_name (app_tracker.tests.test_models.DjangoModelModelTest.test_description_verbose_name) ... ok
test_dunder_string_method (app_tracker.tests.test_models.DjangoModelModelTest.test_dunder_string_method) ... ok
test_is_current_model_default_false (app_tracker.tests.test_models.DjangoModelModelTest.test_is_current_model_default_false) ... ok
test_is_current_model_help_text (app_tracker.tests.test_models.DjangoModelModelTest.test_is_current_model_help_text) ... ok
test_is_current_model_verbose_name (app_tracker.tests.test_models.DjangoModelModelTest.test_is_current_model_verbose_name) ... ok
test_name_help_text (app_tracker.tests.test_models.DjangoModelModelTest.test_name_help_text) ... ok
test_name_max_length (app_tracker.tests.test_models.DjangoModelModelTest.test_name_max_length) ... ok
test_name_unique_true (app_tracker.tests.test_models.DjangoModelModelTest.test_name_unique_true) ... ok
test_name_verbose_name (app_tracker.tests.test_models.DjangoModelModelTest.test_name_verbose_name) ... ok
test_application_field (app_tracker.tests.test_models.LabelModelTest.test_application_field)
Application field should have the following properties: ... ok
test_description_field (app_tracker.tests.test_models.LabelModelTest.test_description_field)
Description field should have the following properties: ... ok
test_dunder_string_method (app_tracker.tests.test_models.LabelModelTest.test_dunder_string_method)
The dunder string method should return the label's name. ... ok
test_hue_field (app_tracker.tests.test_models.LabelModelTest.test_hue_field)
Hue field should have the following properties: ... ok
test_name_field (app_tracker.tests.test_models.LabelModelTest.test_name_field)
Name field should have the following properties: ... ok
test_dunder_string_method (app_tracker.tests.test_models.LanguageFrameworkSystemModelTest.test_dunder_string_method) ... ok
test_meta_verbose_name_plural (app_tracker.tests.test_models.LanguageFrameworkSystemModelTest.test_meta_verbose_name_plural) ... ok
test_name_help_text (app_tracker.tests.test_models.LanguageFrameworkSystemModelTest.test_name_help_text) ... ok
test_name_max_length (app_tracker.tests.test_models.LanguageFrameworkSystemModelTest.test_name_max_length) ... ok
test_name_unique_true (app_tracker.tests.test_models.LanguageFrameworkSystemModelTest.test_name_unique_true) ... ok
test_name_verbose_name (app_tracker.tests.test_models.LanguageFrameworkSystemModelTest.test_name_verbose_name) ... ok
test_application_related_name (app_tracker.tests.test_models.NoteModelTest.test_application_related_name) ... ok
test_application_verbose_name (app_tracker.tests.test_models.NoteModelTest.test_application_verbose_name) ... ok
test_content_verbose_name (app_tracker.tests.test_models.NoteModelTest.test_content_verbose_name) ... ok
test_dunder_string_method (app_tracker.tests.test_models.NoteModelTest.test_dunder_string_method) ... ok
test_title_max_length (app_tracker.tests.test_models.NoteModelTest.test_title_max_length) ... ok
test_title_verbose_name (app_tracker.tests.test_models.NoteModelTest.test_title_verbose_name) ... ok
test_applications_blank_true (app_tracker.tests.test_models.OrganizationalConceptModelTest.test_applications_blank_true)
`applications` field attribute `blank` attribute should be `True`. ... ok
test_applications_help_text (app_tracker.tests.test_models.OrganizationalConceptModelTest.test_applications_help_text) ... ok
test_applications_uses_correct_model (app_tracker.tests.test_models.OrganizationalConceptModelTest.test_applications_uses_correct_model)
`applications` field should use the `Application` model. ... ok
test_applications_verbose_name (app_tracker.tests.test_models.OrganizationalConceptModelTest.test_applications_verbose_name) ... ok
test_description_blank_true (app_tracker.tests.test_models.OrganizationalConceptModelTest.test_description_blank_true) ... ok
test_description_help_text (app_tracker.tests.test_models.OrganizationalConceptModelTest.test_description_help_text) ... ok
test_description_null_true (app_tracker.tests.test_models.OrganizationalConceptModelTest.test_description_null_true) ... ok
test_description_verbose_name (app_tracker.tests.test_models.OrganizationalConceptModelTest.test_description_verbose_name) ... ok
test_dunder_string_method (app_tracker.tests.test_models.OrganizationalConceptModelTest.test_dunder_string_method) ... ok
test_meta_verbose_name (app_tracker.tests.test_models.OrganizationalConceptModelTest.test_meta_verbose_name) ... ok
test_meta_verbose_name_plural (app_tracker.tests.test_models.OrganizationalConceptModelTest.test_meta_verbose_name_plural) ... ok
test_name_help_text (app_tracker.tests.test_models.OrganizationalConceptModelTest.test_name_help_text) ... ok
test_name_max_length (app_tracker.tests.test_models.OrganizationalConceptModelTest.test_name_max_length) ... ok
test_name_unique_true (app_tracker.tests.test_models.OrganizationalConceptModelTest.test_name_unique_true) ... ok
test_name_verbose_name (app_tracker.tests.test_models.OrganizationalConceptModelTest.test_name_verbose_name) ... ok
test_description_blank_true (app_tracker.tests.test_models.ProjectModelTest.test_description_blank_true) ... ok
test_description_help_text (app_tracker.tests.test_models.ProjectModelTest.test_description_help_text) ... ok
test_description_null_true (app_tracker.tests.test_models.ProjectModelTest.test_description_null_true) ... ok
test_description_verbose_name (app_tracker.tests.test_models.ProjectModelTest.test_description_verbose_name) ... ok
test_dunder_string_method (app_tracker.tests.test_models.ProjectModelTest.test_dunder_string_method) ... ok
test_name_help_text (app_tracker.tests.test_models.ProjectModelTest.test_name_help_text) ... ok
test_name_max_length (app_tracker.tests.test_models.ProjectModelTest.test_name_max_length) ... ok
test_name_unique_true (app_tracker.tests.test_models.ProjectModelTest.test_name_unique_true) ... ok
test_name_verbose_name (app_tracker.tests.test_models.ProjectModelTest.test_name_verbose_name) ... ok
test_owner_help_text (app_tracker.tests.test_models.ProjectModelTest.test_owner_help_text) ... ok
test_owner_related_name (app_tracker.tests.test_models.ProjectModelTest.test_owner_related_name) ... ok
test_owner_uses_correct_model (app_tracker.tests.test_models.ProjectModelTest.test_owner_uses_correct_model)
`owner` field should use the `User` model. ... ok
test_owner_verbose_name (app_tracker.tests.test_models.ProjectModelTest.test_owner_verbose_name) ... ok
test_home_view_url_accessible_by_name (app_tracker.tests.test_views.HomeViewTest.test_home_view_url_accessible_by_name)
Test that the `home` view is rendered at the desired location by ... ok
test_home_view_url_exists_at_desired_location (app_tracker.tests.test_views.HomeViewTest.test_home_view_url_exists_at_desired_location)
Test that the `home` view is rendered at "/app-tracker/". ... ok
test_home_view_uses_correct_context (app_tracker.tests.test_views.HomeViewTest.test_home_view_uses_correct_context)
Test that the `home` view uses the correct context. ... ok
test_home_view_uses_correct_template (app_tracker.tests.test_views.HomeViewTest.test_home_view_uses_correct_template)
Test that the `home` view uses the correct template "app_tracker/home.html". ... ok

----------------------------------------------------------------------
Ran 204 tests in 8.942s

OK (skipped=1)
Destroying test database for alias 'default' ('file:memorydb_default?mode=memory&cache=shared')...
(personal-assistant) flynntknapp@DELL-DESK:~/Programming/personal-assistant$
```
