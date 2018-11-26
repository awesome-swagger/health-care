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
  public plans = [
    {
      name: 'Remote Patient Management',
      icon: 'ss-satellitedish',
      description: 'Remote Patient Managment (RPM) care plans are designed to allow care givers to monitor patient health data.',
    },
    {
      name: 'Behavioral Health Initiative',
      icon: 'icomoon-bhi',
      description: 'Behavioral Health Initiative (BHI) care plans are designed for behavioral health care management between one provider and one patient.',
    },
    {
      name: 'Psychiatric Collaborative Care Management',
      icon: 'icomoon-cocm',
      description: 'Psychiatric Collaberative Care Management (CoCM) care plans are for a tiad of care between a PCP, behavioral health care manager, and psychiatric consultant.',
    },
    {
      name: 'Chronic Care Management',
      icon: 'ss-heart',
      description: 'Chronic Care Mangement (CCM) care plans are for patients with two or more chornic conditions who are not considered complex patients.',
    },
    {
      name: 'Complex Chronic Care Management',
      icon: 'ss-addheart',
      description: 'Complex Chronic Care Management (CCCM) care plans are designed for patients with two or more chronic conditions who are considered complex patients.',
    },
    {
      name: 'Transitional Care Management',
      icon: 'ss-signpost',
      description: 'Transitional Care Management (TCM) care plans are designed to support the patient between the transition of care from one care provider to another.',
    },
  ];

  public selectedPlan = {
    name: 'Remote Patient Management',
    icon: 'ss-satellitedish',
    description: 'Remote Patient Managment (RPM) care plans are designed to allow care givers to monitor patient health data.',
  };


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
