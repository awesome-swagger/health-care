import { Component, OnInit } from '@angular/core';
import { FormGroup, FormControl } from '@angular/forms';
import { omit as _omit } from 'lodash';
import { ModalService } from '../../../modules/modals';
import { StoreService } from '../../../services';

@Component({
  selector: 'app-create-vital',
  templateUrl: './create-vital.component.html',
  styleUrls: ['./create-vital.component.scss'],
})
export class CreateVitalComponent implements OnInit {

  public data = null;

  public vital: any = {};
  public vitalForm: FormGroup;
  public tooltipCVM0Open;
  public tooltipCVM1Open;

  public measures = [];

  constructor(
    private modal: ModalService,
    private store: StoreService,
  ) { }

  public ngOnInit() {
    console.log(this.data);
    if (this.data) {
      this.vital = this.data.vital ? this.data.vital : {};
      if (this.vital.questions) {
        this.vital.questions.forEach((obj) => {
          if (obj.answer_type === 'float') {
            obj.answer_type = 'number';
            obj.number_type = 'float';
          } else if (obj.answer_type === 'integer') {
            obj.answer_type = 'number';
            obj.number_type = 'integer';
          }
        });
      }
      this.initForm(this.vital);
    }
  }

  public initForm(vital) {
    this.vitalForm = new FormGroup({
      name: new FormControl(vital.name),
    });
  }

  public answerTypeIsNumber(answerType) {
    return answerType === 'number' || answerType === 'float' || answerType === 'integer';
  }

  public addMetricLine() {
    if (!this.vital.questions) {
      this.vital.questions = [];
    }
    this.vital.questions.push({
      prompt: '',
      answer_type: 'boolean',
      number_type: 'integer',
    });
  }

  public createQuestion(question) {
    let promise = new Promise((resolve, reject) => {
      let createSub = this.store.VitalsQuestions.create(question).subscribe(
        (res) => resolve(res),
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
      let updateSub = this.store.VitalsQuestions.update(question.id, question, true).subscribe(
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
    if (!this.vital.questions) {
      return;
    }
    let promises = [];
    this.vital.questions.forEach((question, i) => {
      question.vital_task_template = this.vital.id;
      if (question.answer_type === 'number') {
        question.answer_type = question.number_type;
      }
      if (!question.id) {
        promises.push(this.createQuestion(question));
      } else {
        promises.push(this.updateQuestion(question));
      }
    });
    return Promise.all(promises);
  }

  public updateVital() {
    let keys = Object.keys(this.vital);
    keys.forEach((key) => {
     if (this.vitalForm.value[key] != undefined) {
        this.vital[key] = this.vitalForm.value[key];
      }
    });
    let promise = new Promise((resolve, reject) => {
      this.vital = Object.assign({}, this.vital, {
        plan_template: this.data.planTemplateId,
        start_on_day: 0,
        appear_time: '00:00:00',
        due_time: '00:00:00',
      });
      let vitalWithoutQuestions = _omit(this.vital, 'questions');
      if (this.vital.id) {
        let updateSub = this.store.VitalsTaskTemplate.update(vitalWithoutQuestions.id, vitalWithoutQuestions, true)
          .subscribe(
            (res) => resolve(res),
            (err) => reject(err),
            () => {
              updateSub.unsubscribe();
            }
          );
      } else {
        let createSub = this.store.VitalsTaskTemplate.create(vitalWithoutQuestions)
          .subscribe(
            (res) => resolve(res),
            (err) => reject(err),
            () => {
              createSub.unsubscribe();
            }
          );
      }
    });
    return promise;
  }

  public clickSave() {
    if (!this.vital.questions || !this.vital.name) {
      return;
    }
    this.updateVital().then((vital: any) => {
      this.vital.id = vital.id;
      this.createOrUpdateAllQuestions().then(() => {
        this.modal.close(null);
      });
    });
  }

  public clickCancel() {
    this.modal.close(null);
  }
}
