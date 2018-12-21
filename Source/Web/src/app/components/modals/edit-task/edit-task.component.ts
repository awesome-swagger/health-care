import { Component, OnInit } from '@angular/core';
import { ModalService } from '../../../modules/modals';
import { FormGroup, FormControl } from '@angular/forms';
import { ERROR_COLLECTOR_TOKEN } from '@angular/platform-browser-dynamic/src/compiler_factory';
import { StoreService } from '../../../services';

@Component({
  selector: 'app-edit-task',
  templateUrl: './edit-task.component.html',
  styleUrls: ['./edit-task.component.scss'],
})
export class EditTaskComponent implements OnInit {

  public data = null;
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
    },
  ];

  constructor(
    private modal: ModalService,
    private store: StoreService
  ) { }

  public ngOnInit() {
    this.data = this.data || {};
    this.task = this.data && this.data.task ? this.data.task : {};
    this.initForm(this.task);
    if (this.getTaskType().type === 'team') {
      this.fetchRoles().then((roles: any) => {
        this.rolesChoices = roles;
      });
    }
  }

  public getTaskType() {
    if (!this.data || !this.data.type) {
      return this.typeChoices[0];
    } else {
      return this.typeChoices.find((obj) => obj.type === this.data.type);
    }
  }

  public updateTaskName() {
    if (!this.task) {
      return;
    }
    let keys = Object.keys(this.task);
    keys.forEach((key) => {
     if (this.nameForm.value[key] != undefined) {
        this.task[key] = this.nameForm.value[key];
      }
    });
    let updateSub = this.getTaskType().dataModel.update(this.task.id, {
      name: this.task.name,
    }).subscribe(
      (task) => {
        this.editName = false;
      },
      (err) => {},
      () => {
        updateSub.unsubscribe();
      }
    );
  }

  public initForm(task) {
    this.nameForm = new FormGroup({
      name: new FormControl(task.name),
    });
    this.taskForm = new FormGroup({
      start_on_day: new FormControl(task.start_on_day),
      frequency: new FormControl(task.frequency),
      repeat_amount_input: new FormControl(task.repeat_amount >=0 ? task.repeat_amount : 0),
      repeat_amount: new FormControl(task.repeat_amount),
      appear_time: new FormControl(task.appear_time),
      due_time: new FormControl(task.due_time),
    });
    if (this.getTaskType().type === 'manager' || this.getTaskType().type === 'team') {
      this.taskForm.addControl('category', new FormControl(task.category));
    }
    if (this.getTaskType().type === 'team') {
      this.taskForm.addControl('role', new FormControl(task.role));
    }
  }

  public updateFormFields() {
    let keys = Object.keys(this.task);
    keys.forEach((key) => {
     if (this.taskForm.value[key] != undefined) {
        if (key === 'repeat_amount' && this.taskForm.value['repeat_amount'] != -1){
          this.task[key] = this.taskForm.value['repeat_amount_input'];
        } else {
          this.task[key] = this.taskForm.value[key];
        }
      }
    });
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

  public createTask() {
    let createSub = this.getTaskType().dataModel.create(this.task).subscribe(
      (task) => {
        this.modal.close(task);
      },
      (err) => {},
      () => {
        createSub.unsubscribe();
      },
    );
  }

  public updateTask() {
    let updateSub = this.getTaskType().dataModel.update(this.task.id, this.task, true).subscribe(
      (task) => {
        this.modal.close(task);
      },
      (err) => {},
      () => {
        updateSub.unsubscribe();
      },
    );
  }

  public submitTask() {
    this.updateFormFields();
    if (this.getTaskType().type === 'manager') {
      this.task.is_manager_task = true;
    }
    if (this.getTaskType().type === 'symptom') {
      if (!this.task.id) {
        this.createTask();
      } else {
        this.updateTask();
      }
    } else {
      this.updateTask();
    }
  }

  public close() {
    this.modal.close(null);
  }
}
