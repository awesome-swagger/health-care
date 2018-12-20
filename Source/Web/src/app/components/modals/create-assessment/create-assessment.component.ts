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
  public assessment = null;
  public assessmentTracking = null;

  constructor(
    private modal: ModalService,
    private store: StoreService,
  ) {

  }

  public ngOnInit() {
    console.log(this.data);
    if (this.data) {
      this.assessment = this.data.assessment ? this.data.assessment : null;
      if (this.assessment) {
        if (this.assessment.tracks_outcome) {
          this.assessmentTracking = 'outcome';
        } else if (this.assessment.tracks_satisfaction) {
          this.assessmentTracking = 'satisfaction';
        }
      }
    }
  }

  public addQuestionLine() {
    if (!this.assessment.questions) {
      this.assessment.questions = [];
    }
    this.assessment.questions.push({
      assessment_task_template: this.assessment.id,
      prompt: '',
      worst_label: '',
      best_label: '',
    });
  }

  public createQuestion(question) {
    let promise = new Promise((resolve, reject) => {
      let createSub = this.store.AssessmentQuestion.create(question).subscribe(
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
      let updateSub = this.store.AssessmentQuestion.update(question.id, question, true).subscribe(
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
      this.assessment.tracks_outcome = tracksOutcome;
      this.assessment.tracks_satisfaction = tracksSatisfaction;
      let assessmentWithoutQuestions = _omit(this.assessment, 'questions');
      let updateSub = this.store.AssessmentTaskTemplate.update(assessmentWithoutQuestions.id, assessmentWithoutQuestions, true)
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

  public clickSave() {
    if (!this.assessment.questions || !this.assessment.name) {
      return;
    }
    this.updateAssessment().then(() => {
      this.createOrUpdateAllQuestions().then(() => {
        this.modal.close(null);
      });
    });
  }
}
