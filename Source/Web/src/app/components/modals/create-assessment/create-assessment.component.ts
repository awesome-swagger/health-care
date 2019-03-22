import { Component, OnInit } from '@angular/core';
import { omit as _omit } from 'lodash';
import { ModalService } from '../../../modules/modals';
import { StoreService } from '../../../services';

@Component({
  selector: 'app-create-assessment',
  templateUrl: './create-assessment.component.html',
  styleUrls: ['./create-assessment.component.scss'],
})
export class CreateAssessmentComponent implements OnInit {

  public data = null;
  public isEditing = false;
  public assessment = null;
  public assessmentTracking = null;
  public nameInput = '';

  constructor(
    private modal: ModalService,
    private store: StoreService,
  ) { }

  public tooltipCAM0Open;

  public ngOnInit() {
    console.log(this.data);
    if (this.data) {
      this.assessment = this.data.assessment ? this.data.assessment : {};
      this.isEditing = this.data.isEditing ? this.data.isEditing : false;
      if (this.assessment) {
        this.nameInput = this.assessment.name;
        if (this.assessment.tracks_outcome) {
          this.assessmentTracking = 'outcome';
        } else if (this.assessment.tracks_satisfaction) {
          this.assessmentTracking = 'satisfaction';
        }
        if (this.assessment.questions) {
          let sortedQuestions = this.sortQuestions(this.assessment.questions);
          sortedQuestions.forEach((obj, index) => {
            obj.order = index;
          });
        }
      }
    }
  }

  public addQuestionLine() {
    let maxOrder = -1;
    if (!this.assessment.questions || this.assessment.questions.length < 1) {
      this.assessment.questions = [];
      maxOrder = -1;
    } else {
      maxOrder = Math.max(...this.assessment.questions.map((obj) => obj.order).sort((a, b) => -(b - a)));
    }
    this.assessment.questions.push({
      prompt: '',
      worst_label: '',
      best_label: '',
      order: maxOrder + 1,
    });
  }

  public moveUp(question) {
    let questionsAtNewOrder = this.assessment.questions.filter((obj) => obj.order === (question.order - 1));
    questionsAtNewOrder.forEach((q) => {
      q.order++;
    });
    question.order--;
  }

  public moveDown(question) {
    let questionsAtNewOrder = this.assessment.questions.filter((obj) => obj.order === (question.order + 1));
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
      let createSub = this.store.AssessmentQuestion.create(question).subscribe(
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
      let updateSub = this.store.AssessmentQuestion.update(question.id, _omit(question, 'id'), true).subscribe(
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
    if (!this.assessment.questions) {
      return;
    }
    let promises = [];
    this.assessment.questions.forEach((question, i) => {
      question.assessment_task_template = this.assessment.id;
      if (!question.id) {
        promises.push(this.createQuestion(question));
      } else {
        promises.push(this.updateQuestion(question));
      }
    });
    return Promise.all(promises);
  }

  public updateAssessment() {
    let promise = new Promise((resolve, reject) => {
      let tracksOutcome = this.assessmentTracking === 'outcome';
      let tracksSatisfaction = this.assessmentTracking === 'satisfaction';
      this.assessment = Object.assign({}, this.assessment, {
        name: this.nameInput,
        tracks_outcome: tracksOutcome,
        tracks_satisfaction: tracksSatisfaction,
      });
      let assessmentWithoutQuestions = _omit(this.assessment, 'questions');
      let updateSub = this.store.AssessmentTaskTemplate.update(assessmentWithoutQuestions.id, _omit(assessmentWithoutQuestions, 'id'), true)
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
      this.store.AssessmentQuestion.destroy(question.id).subscribe(() => {
        let index = this.assessment.questions.findIndex((obj) => obj.id && obj.id === question.id);
        this.assessment.questions.splice(index, 1);
        // Reset order on all questions
        let sortedQuestions = this.sortQuestions(this.assessment.questions);
        sortedQuestions.forEach((obj, index) => {
          obj.order = index;
        });
      });
    } else {
      let index = this.assessment.questions.findIndex((obj) => obj.order === question.order);
      this.assessment.questions.splice(index, 1);
      // Reset order on all questions
      let sortedQuestions = this.sortQuestions(this.assessment.questions);
      sortedQuestions.forEach((obj, index) => {
        obj.order = index;
      });
    }
  }

  public clickSave() {
    if (!this.assessment.questions || !this.nameInput) {
      return;
    }
    this.updateAssessment().then((assessment: any) => {
      this.createOrUpdateAllQuestions().then(() => {
        this.modal.close(this.assessment);
      });
    });
  }

  public clickCancel() {
    this.modal.close(null);
  }
}
