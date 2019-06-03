import { Component, OnInit } from '@angular/core';
import { ModalService } from '../../../modules/modals';
import { FormGroup, FormControl } from '@angular/forms';
import { ERROR_COLLECTOR_TOKEN } from '@angular/platform-browser-dynamic/src/compiler_factory';
import { omit as _omit } from 'lodash';
import { StoreService } from '../../../services';

@Component({
  selector: 'app-edit-task',
  templateUrl: './edit-task.component.html',
  styleUrls: ['./edit-task.component.scss'],
})
export class EditTaskComponent implements OnInit {

  public data = null;
  public isAdhoc = false;
  public totalPatients = 0;
  public frequencyOptions: Array<any> = [
    {displayName: 'Once', value: 'once'},
    {displayName: 'Daily', value: 'daily'},
    {displayName: 'Every Other Day', value: 'every_other_day'},
    {displayName: 'Weekly', value: 'weekly'},
    {displayName: 'Weekdays', value: 'weekdays'},
    {displayName: 'Weekends', value: 'weekends'},
  ];
  public task = null;
  public nameForm: FormGroup;
  public taskForm: FormGroup;
  public editName = false;
  public rolesChoices = [];
  public rolesSelected = [];
  public symptomChoices = [];
  public symptomsSelected = [];
  public categoriesChoices = ['notes', 'interaction', 'coordination'];

  public typeChoices = [
    {
      type: 'manager',
      title: 'Edit CM Task',
      dataModel: this.store.TeamTaskTemplate,
    },
    {
      type: 'team',
      title: 'Edit CT Task',
      dataModel: this.store.TeamTaskTemplate,
    },
    {
      type: 'patient',
      title: 'Edit Patient Task',
      dataModel: this.store.PatientTaskTemplate,
    },
    {
      type: 'assessment',
      title: 'Edit Assessment',
      dataModel: this.store.AssessmentTaskTemplate,
      questionModel: this.store.AssessmentQuestion,
      questionRelatedField: 'assessment_task_template',
    },
    {
      type: 'symptom',
      title: 'Edit Symptom',
      dataModel: this.store.SymptomTaskTemplate,
    },
    {
      type: 'vital',
      title: 'Edit Vital',
      dataModel: this.store.VitalsTaskTemplate,
      questionModel: this.store.VitalsQuestions,
      questionRelatedField: 'vital_task_template',
    },
    {
      type: 'medication',
      title: 'Edit Medication Task',
      dataModel: this.store.MedicationTaskTemplate,
    },
    {
      type: 'plan-manager',
      title: 'Edit CM Task',
      dataModel: this.store.TeamTaskTemplate,
      relatedModel: this.store.PlanTeamTemplate,
      relatedField: 'team_task_template',
    },
    {
      type: 'plan-team',
      title: 'Edit CT Task',
      dataModel: this.store.TeamTaskTemplate,
      relatedModel: this.store.PlanTeamTemplate,
      relatedField: 'team_task_template',
    },
    {
      type: 'plan-patient',
      title: 'Edit Patient Task',
      dataModel: this.store.PatientTaskTemplate,
      relatedModel: this.store.PlanPatientTemplate,
      relatedField: 'patient_task_template',
    },
    {
      type: 'plan-assessment',
      title: 'Edit Assessment',
      dataModel: this.store.AssessmentTaskTemplate,
      relatedModel: this.store.PlanAssessmentTemplate,
      relatedField: 'assessment_task_template',
      questionModel: this.store.AssessmentQuestion,
      questionRelatedField: 'assessment_task_template',
    },
    {
      type: 'plan-symptom',
      title: 'Edit Symptom',
      dataModel: this.store.SymptomTaskTemplate,
      relatedModel: this.store.PlanSymptomTemplate,
      relatedField: 'symptom_task_template',
    },
    {
      type: 'plan-vital',
      title: 'Edit Vital',
      dataModel: this.store.VitalsTaskTemplate,
      relatedModel: this.store.PlanVitalTemplate,
      relatedField: 'vital_task_template',
      questionModel: this.store.VitalsQuestions,
      questionRelatedField: 'vital_task_template',
    },
  ];
  public adhocTypes = ['plan-manager', 'plan-team', 'plan-patient', 'plan-assessment', 'plan-symptom', 'plan-vital'];
  public appearTimeHelpOpen = false;
  public dueTimeHelpOpen = false;
  public categoryHelpOpen = false;
  public symptomsDropOpen = false;
  public roleHelpOpen = false;
  public roleDropOpen = false;

  constructor(
    private modal: ModalService,
    private store: StoreService
  ) { }

  public ngOnInit() {
    if (this.data) {
      console.log(this.data);
      if (this.adhocTypes.includes(this.data.type)) {
        this.isAdhoc = true;
      }
      this.task = this.data && this.data.task ? this.data.task : {};
      this.totalPatients = this.data.totalPatients ? this.data.totalPatients : 0;
      this.initForm(this.task);
    }
  }

  public getTaskType() {
    if (!this.data || !this.data.type) {
      return this.typeChoices[0];
    } else {
      return this.typeChoices.find((obj) => obj.type === this.data.type);
    }
  }

  public getRelatedModel() {
    return this.task[this.getTaskType().relatedField];
  }

  public getTaskName() {
    return this.task.name;
  }

  public updateTaskName() {
    if (!this.task) {
      return;
    }
    let id = null;
    if (this.task.id) {
      id = this.task.id;
    }
    this.task.name = this.nameForm.value['name'];
    if (!this.isAdhoc) {
      if (id) {
        let updateSub = this.getTaskType().dataModel.update(id, {
          name: this.nameForm.value['name'],
        }, true).subscribe(
          (task) => {
            this.editName = false;
          },
          (err) => {},
          () => {
            updateSub.unsubscribe();
          }
        );
      }
    } else {
      if (id) {
        let updateSub = this.getTaskType().relatedModel.update(id, {
          custom_name: this.nameForm.value['name'],
        }, true).subscribe(
          (task) => {
            this.editName = false;
          },
          (err) => {},
          () => {
            updateSub.unsubscribe();
          }
        );
      }
    }
    this.editName = false;
  }

  public initForm(task) {
    if (task.name) {
      this.nameForm = new FormGroup({
        name: new FormControl(task.name),
      });
    }
    this.taskForm = new FormGroup({
      start_on_day: new FormControl(task.start_on_day),
      frequency: new FormControl(task.frequency),
      repeat_amount_input: new FormControl(task.repeat_amount >=0 ? task.repeat_amount : 0),
      repeat_amount: new FormControl(task.repeat_amount),
      appear_time: new FormControl(task.appear_time),
      due_time: new FormControl(task.due_time),
    });
    if (this.getTaskType().type === 'symptom' || this.getTaskType().type === 'plan-symptom') {
      let defaultSymptomIds = [];
      if (task.default_symptoms) {
        defaultSymptomIds = task.default_symptoms.map((obj) => obj.id);
      } else {
        defaultSymptomIds = [];
        task.default_symptoms = [];
      }
      this.taskForm.addControl('default_symptoms', new FormControl(defaultSymptomIds));
      this.fetchSymptoms().then((symptoms: any) => {
        this.symptomChoices = symptoms;
        if (task.default_symptoms) {
          this.symptomsSelected = task.default_symptoms;
        }
      });
    }
    if (this.isTeamTask()) {
      let categoryValue = null;
      if (task.category) {
        categoryValue = task.category;
      } else if (task.team_task_template && task.team_task_template.category) {
        categoryValue = task.team_task_template.category;
      }
      this.taskForm.addControl('category', new FormControl(categoryValue));
    }
    if (this.getTaskType().type === 'team' || this.getTaskType().type === 'plan-team') {
      let roleIds = [];
      if (task.roles) {
        roleIds = task.roles.map((obj) => obj.id);
      } else if (task.team_task_template && task.team_task_template.roles) {
        roleIds = task.team_task_template.roles.map((obj) => obj.id);
      } else {
        roleIds = [];
        task.roles = [];
      }
      this.taskForm.addControl('roles', new FormControl(roleIds));
      this.fetchRoles().then((roles: any) => {
        this.rolesChoices = roles;
        if (task.roles) {
          this.rolesSelected = task.roles;
        } else if (task.team_task_template && task.team_task_template.roles) {
          this.rolesSelected = task.team_task_template.roles;
        }
      });
    }
  }

  public updateFormFields() {
    let keys = Object.keys(this.task);
    let customFields = [
      'name', 'start_on_day', 'frequency', 'repeat_amount', 'appear_time',
      'due_time', 'default_symptoms', 'instructions', 'category'];
    keys.forEach((key) => {
     if (this.taskForm.value[key] != undefined) {
        if (key === 'repeat_amount' && this.taskForm.value['repeat_amount'] != -1) {
          if (!this.isAdhoc) {
            this.task[key] = this.taskForm.value['repeat_amount_input'];
          } else {
            this.task['custom_' + key] = this.taskForm.value['repeat_amount_input'];
          }
        } else {
          if (!this.isAdhoc) {
            this.task[key] = this.taskForm.value[key];
          } else if (customFields.includes(key)) {
            this.task['custom_' + key] = this.taskForm.value[key];
          }
        }
      }
    });
  }

  public fetchSymptoms() {
    let promise = new Promise((resolve, reject) => {
      let symptomsSub = this.store.Symptom.readListPaged().subscribe(
        (symptoms) => resolve(symptoms),
        (err) => reject(err),
        () => {
          symptomsSub.unsubscribe();
        },
      );
    });
    return promise;
  }

  public fetchRoles() {
    let promise = new Promise((resolve, reject) => {
      let rolesSub = this.store.ProviderRole.readListPaged().subscribe(
        (roles) => resolve(roles),
        (err) => reject(err),
        () => {
          rolesSub.unsubscribe();
        },
      );
    });
    return promise;
  }

  public isSymptomSelected(symptom) {
    return this.symptomsSelected.findIndex((obj) => obj.id === symptom.id) > -1;
  }

  public toggleSymptomSelected(symptom) {
    let index = this.symptomsSelected.findIndex((obj) => obj.id === symptom.id);
    if (index > -1) {
      this.symptomsSelected.splice(index, 1);
    } else {
      this.symptomsSelected.push(symptom);
    }
    let selectedIds = this.symptomsSelected.map((obj) => obj.id);
    this.taskForm.controls['default_symptoms'].setValue(selectedIds);
  }

  public formatSelectedSymptoms() {
    if (!this.symptomsSelected || this.symptomsSelected.length < 1) {
      return '';
    }
    if (this.symptomsSelected.length > 1) {
      return `${this.symptomsSelected[0].name}, +${this.symptomsSelected.length - 1}`
    } else {
      return this.symptomsSelected[0].name;
    }
  }

  public isRoleSelected(role) {
    return this.rolesSelected.findIndex((obj) => obj.id === role.id) > -1;
  }

  public toggleRoleSelected(role) {
    let index = this.rolesSelected.findIndex((obj) => obj.id === role.id);
    if (index > -1) {
      this.rolesSelected.splice(index, 1);
    } else {
      this.rolesSelected.push(role);
    }
    let selectedIds = this.rolesSelected.map((obj) => obj.id);
    this.taskForm.controls['roles'].setValue(selectedIds);
  }

  public formatSelectedRoles() {
    if (!this.rolesSelected || this.rolesSelected.length < 1) {
      return '';
    }
    if (this.rolesSelected.length > 1) {
      return `${this.rolesSelected[0].name}, +${this.rolesSelected.length - 1}`
    } else {
      return this.rolesSelected[0].name;
    }
  }

  public isTeamTask() {
    let teamTaskTypes = ['manager', 'team', 'plan-manager', 'plan-team'];
    return teamTaskTypes.includes(this.getTaskType().type);
  }

  public createQuestion(question) {
    let promise = new Promise((resolve, reject) => {
      let createSub = this.getTaskType().questionModel.create(question).subscribe(
        (res) => {
          question.id = res.id;
          resolve(res);
        },
        (err) => reject(err),
        () => {
          createSub.unsubscribe();
        },
      );
    });
    return promise;
  }

  public updateQuestion(question) {
    let promise = new Promise((resolve, reject) => {
      let updateSub = this.getTaskType().questionModel.update(question.id, _omit(question, 'id'), true).subscribe(
        (res) => resolve(res),
        (err) => reject(err),
        () => {
          updateSub.unsubscribe();
        },
      );
    });
    return promise;
  }

  public createOrUpdateAllQuestions() {
    if (!this.task.questions) {
      return;
    }
    let promises = [];
    this.task.questions.forEach((question, i) => {
      question[this.getTaskType().questionRelatedField] = this.task.id;
      if (!question.id) {
        promises.push(this.createQuestion(question));
      } else {
        promises.push(this.updateQuestion(question));
      }
    });
    return Promise.all(promises);
  }

  public createTask() {
    let promise = new Promise((resolve, reject) => {
      let postData = Object.assign({}, this.task);
      let questions = this.task.questions;
      postData = _omit(postData, 'questions');
      if (!this.isAdhoc) {
        let createSub = this.getTaskType().dataModel.create(postData).subscribe(
          (task) => {
            this.task = Object.assign({}, task, {questions: questions});
            resolve(this.task);
          },
          (err) => reject(err),
          () => {
            createSub.unsubscribe();
          },
        );
      } else {
        if (this.task[this.getTaskType().relatedField]) {
          postData[this.getTaskType().relatedField] = this.task[this.getTaskType().relatedField].id;
        }
        let createSub = this.getTaskType().relatedModel.create(postData).subscribe(
          (task) => {
            this.task = Object.assign({}, task, {questions: questions});
            resolve(this.task);
          },
          (err) => reject(err),
          () => {
            createSub.unsubscribe();
          }
        );
      }
    });
    return promise;
  }

  public updateTask() {
    let promise = new Promise((resolve, reject) => {
      let postData = Object.assign({}, this.task);
      let questions = this.task.questions;
      postData = _omit(postData, 'questions');
      if (this.getTaskType().type === 'medication') {
        postData = _omit(postData, 'patient_medication');
      }
      postData = _omit(postData, 'id');
      if (!this.isAdhoc) {
        let updateSub = this.getTaskType().dataModel.update(this.task.id, postData, true).subscribe(
          (task) => {
            this.task = Object.assign({}, task, {questions: questions});
            resolve(this.task);
          },
          (err) => reject(err),
          () => {
            updateSub.unsubscribe();
          },
        );
      } else {
        postData = _omit(postData, this.getTaskType().relatedField);
        let updateSub = this.getTaskType().relatedModel.update(this.task.id, postData, true).subscribe(
          (task) => {
            this.task = Object.assign({}, task, {questions: questions});
            resolve(this.task);
          },
          (err) => reject(err),
          () => {
            updateSub.unsubscribe();
          },
        );
      }
    });
    return promise;
  }

  public submitTask() {
    this.updateFormFields();
    if (this.isAdhoc) {
      this.task.custom_name = this.task.name;
    }
    if (this.getTaskType().type === 'manager') {
      this.task.is_manager_task = true;
    }
    if (this.getTaskType().type === 'plan-manager') {
      this.task.is_manager_task = true;
      this.task.custom_is_manager_task = true;
    }
    if (!this.task.id) {
      this.createTask().then((task) => {
        if (this.getTaskType().type === 'assessment' || this.getTaskType().type === 'vital') {
          this.createOrUpdateAllQuestions().then(() => {
            this.modal.close(this.task);
          });
        } else {
          this.modal.close(task);
        }
      });
    } else {
      this.updateTask().then((task) => {
        if (this.getTaskType().type === 'assessment' || this.getTaskType().type === 'vital') {
          this.createOrUpdateAllQuestions().then(() => {
            this.modal.close(this.task);
          });
        } else {
          this.modal.close(task);
        }
      });
    }
  }

  public close() {
    this.modal.close(null);
  }

  public saveDisabled() {
    if (this.getTaskType().type === 'symptom' || this.getTaskType().type === 'plan-symptom') {
      return this.symptomsSelected.length < 1;
    }
  }
}
