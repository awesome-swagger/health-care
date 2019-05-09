import { Component, OnInit } from '@angular/core';
import {
  groupBy as _groupBy,
  uniqBy as _uniqBy,
  omit as _omit,
} from 'lodash';
import { ModalService } from '../../../modules/modals';
import { StoreService } from '../../../services';
import { CreateAssessmentComponent } from '../create-assessment/create-assessment.component';

@Component({
  selector: 'app-add-assessment',
  templateUrl: './add-assessment.component.html',
  styleUrls: ['./add-assessment.component.scss'],
})
export class AddAssessmentComponent implements OnInit {

  public data = null;
  public totalPatients = 0;
  public isAdhoc = false;
  public assessments = [];
  public searchInput = '';
  public assessmentsShown = [];
  public selectedAssessment = null;
  public createAssessment = false;
  public newAssessmentName = '';

  constructor(
    private modal: ModalService,
    private store: StoreService,
  ) {

  }

  public ngOnInit() {
    console.log(this.data);
    if (this.data) {
      this.totalPatients = this.data.totalPatients ? this.data.totalPatients : 0;
      if (this.data.planTemplateId) {
        this.isAdhoc = false;
      } else if (this.data.planId) {
        this.isAdhoc = true;
      }
      this.store.AssessmentTaskTemplate.readListPaged({
        is_available: true,
      }).subscribe(
        (data) => {
          this.assessments = data;
          this.assessmentsShown = _uniqBy(this.assessments, (obj) => {
            return obj.name;
          });
        },
        (err) => {},
        () => {}
      );
    }
  }

  public filterAssessments() {
    let assessmentMatches = this.assessments.filter((obj) => {
      return obj.name.toLowerCase().indexOf(this.searchInput.toLowerCase()) >= 0;
    });
    this.assessmentsShown = _uniqBy(assessmentMatches, (obj) => obj.name);
  }

  public selectAssessment(assessment) {
    if (assessment.edit || assessment.delete) {
      return;
    }
    this.selectedAssessment = assessment;
  }

  public uniqByNameCount(assessment) {
    let uniqueAssessments = this.assessments.filter(
      (obj) => obj.name === assessment.name
    ).filter(
      (obj) => obj.is_active === true
    );
    return uniqueAssessments.length;
  }

  public clickEditAssessment(assessment, e) {
    e.stopPropagation();
    assessment.edit = !assessment.edit;
    assessment.origName = assessment.name;
  }

  public clickUndoName(assessment, e) {
    e.stopPropagation();
    assessment.edit = !assessment.edit;
    assessment.name = assessment.origName;
  }

  public updateAssessmentName(assessment, e) {
    e.stopPropagation();
    let assessments = this.assessments.filter((obj) => obj.name === assessment.origName || obj.name === assessment.name);
    assessments.forEach((obj) => {
      let updateSub = this.store.AssessmentTaskTemplate.update(obj.id, {
        name: assessment.name,
      }, true).subscribe(
        (resp) => {
          obj.name = assessment.name;
          assessment.edit = false;
        },
        (err) => {},
        () => {
          updateSub.unsubscribe();
        }
      );
    });
  }

  public clickDeleteAssessment(assessment, e) {
    e.stopPropagation();
    assessment.delete = true;
  }

  public clickUndoDelete(assessment, e) {
    e.stopPropagation();
    assessment.delete = false;
  }

  public confirmDeleteAssessment(assessment, e) {
    e.stopPropagation();
    let assessments = this.assessments.filter((obj) => obj.name === assessment.origName || obj.name === assessment.name);
    assessments.forEach((obj) => {
      let updateSub = this.store.AssessmentTaskTemplate.update(obj.id, {
        is_available: false,
        is_active: false
      }, true).subscribe(
        (resp) => {
          let index = this.assessments.findIndex((a) => a.id === resp.id);
          this.assessments.splice(index, 1);
          assessment.delete = false;
          this.assessmentsShown = _uniqBy(this.assessments, (obj) => {
            return obj.name;
          });
        },
        (err) => {},
        () => {
          updateSub.unsubscribe();
        }
      );
    });
  }

  public addAssessment(assessmentName, e) {
    if (assessmentName.length <= 0) {
      return;
    }
    let assessment = {};
    if (!this.isAdhoc) {
      assessment = {
        start_on_day: 0,
        frequency: 'once',
        repeat_amount: -1,
        appear_time: '00:00:00',
        due_time: '00:00:00',
        is_active: true,
        is_available: true,
        name: assessmentName,
        plan_template: this.data.planTemplateId,
        tracks_outcome: false,
        tracks_satisfaction: false,
      }
      this.createAssessment = false;
      this.modal.close(assessment);
    } else {
      assessment = {
        custom_start_on_day: 0,
        custom_frequency: 'once',
        custom_repeat_amount: -1,
        custom_appear_time: '00:00:00',
        custom_due_time: '00:00:00',
        custom_name: assessmentName,
        plan: this.data.planId,
      };
      this.createAssessment = false;
      this.modal.close(assessment);
    }
  }

  public clickNext() {
    let newAssessment: any = {};
    newAssessment = {
      start_on_day: this.selectedAssessment.start_on_day,
      frequency: this.selectedAssessment.frequency,
      repeat_amount: this.selectedAssessment.repeat_amount,
      appear_time: this.selectedAssessment.appear_time,
      due_time: this.selectedAssessment.due_time,
      name: this.selectedAssessment.name,
      is_active: true,
      is_available: true,
      tracks_outcome: this.selectedAssessment.tracks_outcome,
      tracks_satisfaction: this.selectedAssessment.tracks_satisfaction,
    };
    if (!this.isAdhoc) {
      newAssessment['plan_template'] = this.data.planTemplateId;
    } else {
      newAssessment['plan'] = this.data.planId;
      newAssessment['assessment_task_template'] = this.selectedAssessment;
    }
    newAssessment['questions'] = this.selectedAssessment.questions.map((obj) => {
      return _omit(_omit(obj, 'id'), 'assessment_task_template');
    });
    this.createAssessment = false;
    this.modal.close(newAssessment);
  }

  public clickCancel() {
    this.modal.close(null);
  }
}
