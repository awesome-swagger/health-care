import { Component, OnInit } from '@angular/core';
import { ModalService } from '../../../modules/modals';
import { CreateAssessmentComponent } from '../create-assessment/create-assessment.component';

@Component({
  selector: 'app-add-assessment',
  templateUrl: './add-assessment.component.html',
  styleUrls: ['./add-assessment.component.scss'],
})
export class AddAssessmentComponent implements OnInit {

  public data = null;
  public totalPatients = 0;
  public assessmentsList = [];
  public searchInput = '';
  public assessmentsShown = [];
  public selectedAssessment = null;
  public editingTemplate = false;

  constructor(
    private modal: ModalService,
  ) {

  }

  public ngOnInit() {
    console.log(this.data);
    if (this.data) {
      this.editingTemplate = this.data.editingTemplate;
      this.totalPatients = this.data.totalPatients ? this.data.totalPatients : 0;
      this.assessmentsList = this.data.assessmentsList ? this.data.assessmentsList : [];
      this.assessmentsShown = this.assessmentsList;
    }
  }

  public createNewAssessment() {
    this.modal.close('create-new');
  }

  public filterAssessments() {
    this.assessmentsShown = this.assessmentsList.filter((obj) => {
      return obj.name.toLowerCase().indexOf(this.searchInput.toLowerCase()) !== -1;
    });
  }

  public editAssessment(assessment) {
    this.modal.close(assessment);
  }

  public deleteAssessment(assessment) {

  }

  public clickNext() {
    this.modal.close(this.selectedAssessment);
  }

  public clickCancel() {
    this.modal.close(null);
  }
}
