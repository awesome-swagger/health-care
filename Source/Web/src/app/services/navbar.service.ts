import { Injectable } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';

@Injectable()
export class NavbarService {

  public recentPatients = [];
  public planDetailId = null;
  public patientDetailId = null;
  private _instance = null;
  private _visible = true;

  constructor(
    private route: ActivatedRoute,
    private router: Router,
  ) { }

  public hide() {
    this.visible = false;
  }

  public show() {
    this.visible = true;
  }

  public normalState() {
    console.log('normal state');
    this.planDetailId = null;
    this.instance.normalState = true;
    this.instance.planDetailState = false;
    this.instance.patientDetailState = false;
  }

  public planDetailState(id) {
    this.planDetailId = id;
    this.patientDetailId = null;
    this.instance.normalState = false;
    this.instance.planDetailState = true;
    this.instance.patientDetailState = false;
  }

  public patientDetailState(patientId, planId) {
    console.log('patient state');
    this.planDetailId = planId;
    this.patientDetailId = patientId;
    this.instance.normalState = false;
    this.instance.planDetailState = false;
    this.instance.patientDetailState = true;
  }

  public addRecentPatient(patient) {
    if (this.recentPatients.find((obj) => {return obj.id === patient.id})) {
      return;
    }
    this.recentPatients.push(patient);
  }

  public get instance() {
    return this._instance;
  }

  public set instance(value) {
    this._instance = value;
  }

  public get visible() {
    return this._visible;
  }

  public set visible(value) {
    this._visible = value;
  }
}
