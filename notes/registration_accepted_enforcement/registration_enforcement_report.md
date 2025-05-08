# 📝 Registration Enforcement Report

## `boosts/views.py`

### ✅ CBVs with `RegistrationAcceptedMixin`
- InspirationalListView
- InspirationalCreateView

### ❌ CBVs MISSING `RegistrationAcceptedMixin`
- BretBeastieInspirationalListView

### ❌ FBVs MISSING `@registration_accepted_required`
- send_inspirational
- landing_view

---

## `app_tracker/views.py`

### ✅ CBVs with `RegistrationAcceptedMixin`
- OrganizationalConceptListView

### ❌ FBVs MISSING `@registration_accepted_required`
- home

---

## `activity_tracker/views.py`

### ✅ CBVs with `RegistrationAcceptedMixin`
- ActivityListView
- ActivityDetailView

### ❌ FBVs MISSING `@registration_accepted_required`
- json_response
- complete_an_activity_view

---

## `project_manager/views.py`


### ❌ FBVs MISSING `@registration_accepted_required`
- temporary_http_response

---

## `pharma_tracker/views.py`


### ❌ CBVs MISSING `RegistrationAcceptedMixin`
- PharmaceuticalListView

---

## `care_craft/views.py`


### ✅ FBVs with `@registration_accepted_required`
- activity_create
- activity_update
- activity_delete

### ❌ FBVs MISSING `@registration_accepted_required`
- activity_list
- activity_detail

---

## `uc_goals/views.py`

### ✅ CBVs with `RegistrationAcceptedMixin`
- GoalCreateView
- GoalDetailView
- GoalUpdateView
- GoalDeleteView

### ✅ FBVs with `@registration_accepted_required`
- ultimate_concerns
- orphan_goals

---

## `career_organizerator/views.py`

### ✅ CBVs with `RegistrationAcceptedMixin`
- PurposeListView
- SkillListView
- BehavioralInterviewQuestionListView
- QuestionResponseListView
- QuestionResponseCreateView
- QuestionResponseUpdateView
- BulletPointListView

### ❌ FBVs MISSING `@registration_accepted_required`
- home
- skill_move_up
- skill_move_down
- skill_delete

---

## `vitals/views.py`


### ❌ CBVs MISSING `RegistrationAcceptedMixin`
- BloodPressureListView
- BloodPressureCreateView

### ❌ FBVs MISSING `@registration_accepted_required`
- home

---

## `opportunity_search/views.py`

### ✅ CBVs with `RegistrationAcceptedMixin`
- WorkSearchActivityListView

---

## `cbt/views.py`

### ✅ CBVs with `RegistrationAcceptedMixin`
- CognitiveDistortionListView
- ThoughtListView
- ThoughtCreateView
- ThoughtDetailView

### ❌ FBVs MISSING `@registration_accepted_required`
- home

---

## `value_centric/views.py`

### ✅ CBVs with `RegistrationAcceptedMixin`
- PersonalValueCreateView
- PersonalValueDetailView
- PersonalValueUpdateView
- PersonalValueDeleteView
- PersonalValueListView

---

## `accounts/views.py`


### ❌ CBVs MISSING `RegistrationAcceptedMixin`
- ForbiddenView
- CustomUserSignUpView
- CustomLoginView
- CustomUserUpdateView
- CustomUserDetailView

---

## `goals/views.py`

### ✅ CBVs with `RegistrationAcceptedMixin`
- GoalListView

---

## `sonic_text/views.py`

### ✅ CBVs with `RegistrationAcceptedMixin`
- AudioFileListView
- AudioFileDetailView
- AudioFileCreateView
- AudioFileUpdateView
- AudioFileDeleteView

---

## `pi_tracker/views.py`

### ✅ CBVs with `RegistrationAcceptedMixin`
- PiDeviceCreateView
- PiDeviceUpdateView

### ✅ FBVs with `@registration_accepted_required`
- pi_device_list
- pi_device_detail

---

## `unimportant_notes/views.py`

### ✅ CBVs with `RegistrationAcceptedMixin`
- NoteTagDetailView
- NoteTagListView
- UnimportantNoteCreateView
- UnimportantNoteDetailView
- UnimportantNoteUpdateView
- UnimportantNoteListView

---

## `journal/views.py`

### ✅ CBVs with `RegistrationAcceptedMixin`
- EntryCreateView
- EntryDetailView
- EntryUpdateView
- EntryDeleteView
- EntryListView

---

## `self_enquiry/views.py`


### ❌ CBVs MISSING `RegistrationAcceptedMixin`
- JournalCreateView
- JournalListView
- JournalDetailView
- JournalUpdateView
- JournalConfirmDeleteView
- JournalDeleteView

---

