import { Component, OnInit } from '@angular/core';
import {
  groupBy as _groupBy,
  uniqBy as _uniqBy,
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
  public assessments = [];
  public searchInput = '';
  public assessmentsShown = [];
  public selectedAssessment = null;
  public editingTemplate = false;
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
      this.editingTemplate = this.data.editingTemplate;
      this.totalPatients = this.data.totalPatients ? this.data.totalPatients : 0;
      this.store.AssessmentTaskTemplate.readListPaged().subscribe(
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

  public uniqByNameCount(assessment) {
    return this.assessments.filter((obj) => obj.name === assessment.name).length;
  }

  public filterAssessments() {
    let assessmentMatches = this.assessments.filter((obj) => {
      return obj.name.toLowerCase().indexOf(this.searchInput.toLowerCase()) >= 0;
    });
    this.assessmentsShown = _uniqBy(assessmentMatches, (obj) => obj.name);
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

  public clickDeleteAssessment(assessment, e) {
    e.stopPropagation();
  }

  public addAssessment(assessmentName, e) {
    if (assessmentName.length <= 0) {
      return;
    }
    let newAssessment = {
      start_on_day: 0,
      appear_time: '00:00:00',
      due_time: '00:00:00',
      name: assessmentName,
      plan_template: this.data.planTemplateId,
    }
    let createSub = this.store.AssessmentTaskTemplate.create(newAssessment).subscribe(
      (resp) => {
        this.assessments.push(resp);
        this.createAssessment = false;
        this.modal.close(resp);
      },
      (err) => {},
      () => {
        createSub.unsubscribe();
      }
    );
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

  public clickNext() {
    let newAssessment = {
      start_on_day: 0,
      appear_time: '00:00:00',
      due_time: '00:00:00',
      name: this.selectedAssessment.name,
      plan_template: this.data.planTemplateId,
    };
    let createSub = this.store.AssessmentTaskTemplate.create(newAssessment).subscribe(
      (resp) => {
        this.assessments.push(resp);
        this.createAssessment = false;
        this.modal.close(resp);
      },
      (err) => {},
      () => {
        createSub.unsubscribe();
      }
    );
  }

  public clickCancel() {
    this.modal.close(null);
  }
}
