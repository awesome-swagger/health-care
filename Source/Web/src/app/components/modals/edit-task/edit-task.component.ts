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
    {displayName: 'Daily', value: 'daily'},
    {displayName: 'Weekly', value: 'weekly'},
    {displayName: 'Other', value: 'other'},
  ];
  public task;
  public taskForm: FormGroup;

  constructor(
    private modal: ModalService,
    private store: StoreService
  ) { }

  public ngOnInit() {
    this.data = this.data || {};
    this.task = this.data && this.data.task ? this.data.task : {};
    this.initForm(this.task);
  }

  public close() {
    this.modal.close(null);
  }

  public initForm(task) {
    this.taskForm = new FormGroup({
      name: new FormControl(task.name),
      plan_template: new FormControl(task.plan_template),
      start_on_day: new FormControl(task.start_on_day),
      frequency: new FormControl(task.frequency),
      repeat_amount_input: new FormControl(task.repeat_amount >=0? task.repeat_amount: 0),
      repeat_amount: new FormControl(task.repeat_amount),
      appear_time: new FormControl(task.appear_time),
      due_time: new FormControl(task.due_time),
      category: new FormControl(task.category),
      role: new FormControl(task.role),
      is_manager_task: new FormControl(task.is_manager_task),
    });
  }

  public updateRepeatAmount() {
    let keys = Object.keys(this.task);
    keys.forEach((key) => {
     if (this.taskForm.value[key] != undefined) {
        if (key === 'repeat_amount' && this.taskForm.value['repeat_amount'] != -1){
          this.task[key] = this.taskForm.value['repeat_amount_input'];
        }
        else {
          this.task[key] = this.taskForm.value[key];
        }
      }
    });
  }

  public updateTaskName(task) {
    this.store.TeamTaskTemplate.update(task.id,task).subscribe((resp)=> {
       console.log(resp);
    });
  }

  public submitTask() {
    this.updateRepeatAmount();
    // Since this modal is used to update all task types it will close the modal with the updated task as the response.
    // It will then be up to the activated route to decide how to update the template.
    this.modal.close(this.task);
  }
}
