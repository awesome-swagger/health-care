import { Component, OnDestroy, OnInit } from '@angular/core';
import * as moment from 'moment';
import { AuthService, StoreService } from '../../../../services';

@Component({
  selector: 'app-problem-areas',
  templateUrl: './problem-areas.component.html',
  styleUrls: ['./problem-areas.component.scss'],
})
export class ProblemAreasComponent implements OnDestroy, OnInit {

  public data = null;
  public moment = moment;

  public addPA = false;

  public user = null;
  public problemAreas = [];

  public editIndex = -1;
  public deleteIndex = -1;
  public currentEditName = '';
  public currentEditText = '';
  public currentAddName = '';
  public currentAddText = '';

  private authSub = null;

  constructor(
    private auth: AuthService,
    private store: StoreService,
  ) { }

  public ngOnInit() {
    this.authSub = this.auth.user$.subscribe((user) => {
      this.user = user;
    });
    if (this.data) {
      this.problemAreas = this.data.problemAreas ? this.data.problemAreas : [];
    }
  }

  public ngOnDestroy() {
    if (this.authSub) {
      this.authSub.unsubscribe();
    }
  }

  public clickAddProblemArea() {
    this.addPA = true;
    this.currentAddName = '';
    this.currentAddText = '';
  }

  public clickRevert() {
    this.addPA = false;
    this.currentAddName = '';
    this.currentAddText = '';
  }

  public addProblemArea() {
    if (!this.user) {
      return;
    }
    this.store.ProblemArea.create({
      patient: this.data.patient.id,
      plan: this.data.plan.id,
      date_identified: moment().format('YYYY-MM-DD'),
      identified_by: this.user.id,
      name: this.currentAddName,
      description: this.currentAddText,
    }).subscribe((problemArea) => {
      this.problemAreas.push(problemArea);
      this.addPA = false;
      this.currentAddName = '';
      this.currentAddText = '';
    });
  }

  public clickEditProblem(index, problem) {
    this.editIndex = index;
    this.currentEditName = problem.name;
    this.currentEditText = problem.description;
  }

  public clickDeleteProblem(index) {
    this.deleteIndex = index;
  }

  public clickSaveEdit(index) {
    this.editIndex = -1;
    this.store.ProblemArea.update(this.problemAreas[index].id, {
      name: this.currentEditName,
      description: this.currentEditText,
    }).subscribe((updatedProblemArea) => {
      this.problemAreas[index] = updatedProblemArea;
    });
  }

  public confirmDelete(index) {
    this.deleteIndex = -1;
    this.store.ProblemArea.destroy(this.problemAreas[index].id).subscribe(
      () => {
        this.problemAreas.splice(index, 1);
      }
    );
  }
}
