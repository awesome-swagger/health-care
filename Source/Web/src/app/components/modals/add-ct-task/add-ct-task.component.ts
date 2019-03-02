import { Component, OnInit } from '@angular/core';
import { ModalService } from '../../../modules/modals';
import { StoreService } from '../../../services';

@Component({
  selector: 'app-add-ct-task',
  templateUrl: './add-ct-task.component.html',
  styleUrls: ['./add-ct-task.component.scss'],
})
export class AddCTTaskComponent implements OnInit {

  public data = null;
  public totalPatients = 0;
  public tasks = [];
  public searchInput = '';
  public tasksShown = [];
  public selectedTask = null;
  public createTask = false;

  public typeChoices = [
    {
      type: 'manager',
      title: 'Add CM Task',
      dataModel: this.store.TeamTaskTemplate,
    },
    {
      type: 'team',
      title: 'Add CT Task',
      dataModel: this.store.TeamTaskTemplate,
    },
    {
      type: 'patient',
      title: 'Add Patient Task',
      dataModel: this.store.PatientTaskTemplate,
    },
  ];

  constructor(
    private modal: ModalService,
    private store: StoreService
  ) { }

  public ngOnInit() {
    console.log(this.data);
    if (this.data) {
      this.totalPatients = this.data.totalPatients ? this.data.totalPatients : 0;
      this.tasks = this.data.taskList ? this.data.taskList : [];
      this.tasksShown = this.tasks;
    }
  }

  public getTaskType() {
    if (!this.data || !this.data.type) {
      return this.typeChoices[0];
    } else {
      return this.typeChoices.find((obj) => obj.type === this.data.type);
    }
  }

  public updateTaskName(task) {
    let updateSub = this.getTaskType().dataModel.update(task.id, {
      name: task.name,
    }, true).subscribe(
      (resp) => {
        task.edit = false;
      },
      (err) => {},
      () => {
        updateSub.unsubscribe();
      }
    );
  }

  public addTask(taskName) {
    if (taskName.length <= 0) {
      return;
    }
    let task = {
      start_on_day: 0,
      appear_time: '00:00:00',
      due_time: '00:00:00',
      name: taskName,
      plan_template: this.data.planTemplateId,
      category: 'interaction',
      is_manager_task: false,
    }
    if (this.getTaskType().type === 'manager') {
      task.is_manager_task = true;
    }
    let createSub = this.getTaskType().dataModel.create(task).subscribe(
      (resp) =>{
        this.tasks.push(resp);
        this.createTask = false;
        this.modal.close(resp);
      },
      (err) => {},
      () => {
        createSub.unsubscribe();
      }
    );
  }

  public filterTasks() {
    this.tasksShown = this.tasks.filter((obj) => {
      return obj.name.toLowerCase().indexOf(this.searchInput.toLowerCase()) >= 0;
    });
  }

  public next(task) {
    if (!this.selectedTask) {
      return;
    }
    this.modal.close(task);
  }

  public close() {
    this.modal.close(null);
  }
}
