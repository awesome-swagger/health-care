import { Component, OnInit } from '@angular/core';
import { ModalService } from '../../../../modules/modals';
import { StoreService } from '../../../../services';

@Component({
  selector: 'app-care-plan-consent',
  templateUrl: './care-plan-consent.component.html',
  styleUrls: ['./care-plan-consent.component.scss']
})
export class CarePlanConsentComponent implements OnInit {

  public data = null;

  public patient = null;
  public carePlan = null;
  public planConsent: any = {
    verbal_consent: false,
    seen_within_year: false,
    discussed_co_pay: false,
    will_use_mobile_app: false,
    will_interact_with_team: false,
    will_complete_tasks: false,
  };

  constructor(
    private modal: ModalService,
    private store: StoreService,
  ) { }

  public ngOnInit() {
    this.store.CarePlan.read(this.data.plan_id).subscribe((carePlan) => {
      this.carePlan = carePlan;
      this.store.PatientProfile.read(carePlan.patient.id).subscribe((patient) => {
        this.patient = patient;
        this.store.PlanConsentForm.readList({
          plan: this.data.plan_id,
        }).subscribe((consentForms) => {
          if (consentForms.results.length > 0) {
            this.planConsent = consentForms.results[0];
          }
        });
      });
    });
  }

  public clickCancel() {
    this.modal.close(null);
  }

  public clickNext() {
    if (this.planConsent.id) {
      this.store.PlanConsentForm.update(this.planConsent.id, this.planConsent, true).subscribe((consent) => {
        this.modal.close(consent)
      })
    } else {
      this.planConsent.plan = this.carePlan.id;
      this.store.PlanConsentForm.create(this.planConsent).subscribe((consent) => {
        this.modal.close(consent);
      });
    }
  }
}
