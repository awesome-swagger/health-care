import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { ModalService } from '../../../../modules/modals';
import { StoreService } from '../../../../services';

@Component({
  selector: 'app-add-plan',
  templateUrl: './add-plan.component.html',
  styleUrls: ['./add-plan.component.scss'],
})
export class AddPlanComponent implements OnInit {

  public data = null;

  public serviceAreas = [];
  public selectedServiceArea = null;
  public nameInput: string = null;
  public durationInput: number = 6;
  public selectedType: string = null;
  public multiOpen = false;

  constructor(
    private route: ActivatedRoute,
    private router: Router,
    private modals: ModalService,
    private store: StoreService,
  ) {}

  public ngOnInit() {
    console.log(this.data);
    this.getServiceAreas().then((serviceAreas: any) => {
      this.serviceAreas = serviceAreas;
      if (this.data && this.data.serviceAreaId) {
        let match = this.serviceAreas.find((obj) => obj.id === this.data.serviceAreaId);
        this.selectedServiceArea = match;
      }
    });
  }

  public getServiceAreas() {
    let promise = new Promise((resolve, reject) => {
      let serviceAreasSub = this.store.ServiceArea.readListPaged().subscribe(
        (serviceAreas) => {
          resolve(serviceAreas);
        },
        (err) => {
          reject(err);
        },
        () => {
          serviceAreasSub.unsubscribe();
        }
      );
    });
    return promise;
  }

  public clickCancel() {
    this.modals.close(null);
  }

  public continueDisabled() {
    return !this.nameInput || !this.selectedServiceArea;
  }

  public clickContinue() {
    let createSub = this.store.CarePlanTemplate.create({
      name: this.nameInput,
      duration_weeks: this.durationInput,
      service_area: this.selectedServiceArea.id,
    }).subscribe(
      (res) => {
        this.modals.close(null);
        this.router.navigate(['/plan', res.id, 'schedule']);
      },
      (err) => {},
      () => {
        createSub.unsubscribe();
      }
    );
  }
}
