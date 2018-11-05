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

  public planTypes = [];

  public nameInput: string = null;
  public durationInput: number = 6;
  public selectedType: string = null;

  constructor(
    private route: ActivatedRoute,
    private router: Router,
    private modals: ModalService,
    private store: StoreService,
  ) {}

  public ngOnInit() {
    console.log(this.data);
    this.getPlanTypes().then((planTypes: any) => {
      this.planTypes = planTypes;
    });
  }

  public getPlanTypes() {
    let promise = new Promise((resolve, reject) => {
      let typesSub = this.store.CarePlanTemplateType.readListPaged().subscribe(
        (planTypes) => {
          resolve(planTypes);
        },
        (err) => {
          reject(err);
        },
        () => {
          typesSub.unsubscribe();
        }
      );
    });
    return promise;
  }

  public clickCancel() {
    this.modals.close(null);
  }

  public clickContinue() {
    let createSub = this.store.CarePlanTemplate.create({
      name: this.nameInput,
      duration_weeks: this.durationInput,
      type: this.selectedType,
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
