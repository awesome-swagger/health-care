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
  public assessmentsList = [];
  public searchInput = '';
  public assessmentsShown = [];
  public selectedAssessment = null;

  constructor(
    private modal: ModalService,
  ) {

  }

  public ngOnInit() {
    console.log(this.data);
    if (this.data) {
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

  public editAssessmentName() {
    
  }

  public clickNext() {
    this.modal.close(this.selectedAssessment);
  }

  public clickCancel() {
    this.modal.close(null);
  }
}
