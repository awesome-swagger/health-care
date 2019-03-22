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

  public isEditing = false;
  public vital: any = {};
  public vitalForm: FormGroup;

  public syncTooltipOpen = false;
  public typeTooltipOpen = false;

  constructor(
    private modal: ModalService,
    private store: StoreService,
  ) { }

  public ngOnInit() {
    console.log(this.data);
    if (this.data) {
      this.vital = this.data.vital ? this.data.vital : {};
      this.isEditing = this.data.isEditing ? this.data.isEditing : false;
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
        let sortedQuestions = this.sortQuestions(this.vital.questions);
        sortedQuestions.forEach((obj, index) => {
          obj.order = index;
        });
      }
      this.initForm(this.vital);
    }
  }

  public initForm(vital) {
    this.vitalForm = new FormGroup({
      name: new FormControl(vital.name),
      instructions: new FormControl(vital.instructions),
    });
  }

  public clickPreview() {
    this.modal.close({
      'next': 'preview',
      'vital': this.vital,
    });
  }

  public answerTypeIsNumber(answerType) {
    return answerType === 'number' || answerType === 'float' || answerType === 'integer';
  }

  public addMetricLine() {
    let maxOrder = -1;
    if (!this.vital.questions || this.vital.questions.length < 1) {
      this.vital.questions = [];
      maxOrder = -1;
    } else {
      maxOrder = Math.max(...this.vital.questions.map((obj) => obj.order).sort((a, b) => -(b - a)));
    }
    this.vital.questions.push({
      prompt: '',
      answer_type: 'boolean',
      number_type: 'integer',
      order: maxOrder + 1,
    });
  }

  public moveUp(question) {
    let questionsAtNewOrder = this.vital.questions.filter((obj) => obj.order === (question.order - 1));
    questionsAtNewOrder.forEach((q) => {
      q.order++;
    });
    question.order--;
  }

  public moveDown(question) {
    let questionsAtNewOrder = this.vital.questions.filter((obj) => obj.order === (question.order + 1));
    questionsAtNewOrder.forEach((q) => {
      q.order--;
    });
    question.order++;
  }

  public sortQuestions(questions) {
    if (!questions) {
      return [];
    }
    return questions.sort((a, b) => -(b.order - a.order));
  }

  public createQuestion(question) {
    let promise = new Promise((resolve, reject) => {
      let createSub = this.store.VitalsQuestions.create(question).subscribe(
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
      let updateSub = this.store.VitalsQuestions.update(question.id, _omit(question, 'id'), true).subscribe(
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
    let vitalWithoutQuestions = _omit(this.vital, 'questions');
    let updateSub = this.store.VitalsTaskTemplate.update(vitalWithoutQuestions.id, _omit(vitalWithoutQuestions, 'id'), true)
      .subscribe(
        (res) => resolve(res),
        (err) => reject(err),
        () => {
          updateSub.unsubscribe();
        }
      );
    });
    return promise;
  }

  public clickDeleteQuestion(question) {
    if (question.id) {
      this.store.VitalsQuestions.destroy(question.id).subscribe(() => {
        let index = this.vital.questions.findIndex((obj) => obj.id && obj.id === question.id);
        this.vital.questions.splice(index, 1);
        // Reset order on all questions
        let sortedQuestions = this.sortQuestions(this.vital.questions);
        sortedQuestions.forEach((obj, index) => {
          obj.order = index;
        });
      });
    } else {
      let index = this.vital.questions.findIndex((obj) => obj.order && obj.order === question.order);
      this.vital.questions.splice(index, 1);
      // Reset order on all questions
      let sortedQuestions = this.sortQuestions(this.vital.questions);
      sortedQuestions.forEach((obj, index) => {
        obj.order = index;
      });
    }
  }

  public clickSave() {
    if (!this.vital.questions || !this.vital.name) {
      return;
    }
    this.updateVital().then((vital: any) => {
      this.createOrUpdateAllQuestions().then(() => {
        this.modal.close(this.vital);
      });
    });
  }

  public clickCancel() {
    this.modal.close(null);
  }
}
