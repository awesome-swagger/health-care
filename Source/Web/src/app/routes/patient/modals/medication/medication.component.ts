import { Component, OnInit } from '@angular/core';
import { ModalService } from '../../../../modules/modals';
import { StoreService } from '../../../../services';

@Component({
  selector: 'app-medication',
  templateUrl: './medication.component.html',
  styleUrls: ['./medication.component.scss'],
})
export class MedicationComponent implements OnInit {

  public data = null;
  public frequencyOptions: Array<any> = [
    {displayName: 'Once', value: 'once'},
    {displayName: 'Daily', value: 'daily'},
    {displayName: 'Every Other Day', value: 'every_other_day'},
    {displayName: 'Weekly', value: 'weekly'},
    {displayName: 'Weekdays', value: 'weekdays'},
    {displayName: 'Weekends', value: 'weekends'},
  ];
  public plan = null;
  public medications = [];
  public careTeamMembers = [];
  public selectedMedication = null;
  public doseMg = 0;
  public datePrescribed = null;
  public durationDays = 0;
  public prescribingPractitioner = null;
  public instructions = '';

  public startDay = 0;
  public frequency = 'once';
  public repeatsChoice = 'plan_end';
  public repeatAmount = 1;
  public appearTime = '00:00:00';
  public dueTime = '00:00:00';

  public showDate;

  constructor(
    private modal: ModalService,
    private store: StoreService,
  ) {}

  public ngOnInit() {
    console.log(this.data);
    if (this.data) {
      this.plan = this.data.plan;
      this.fetchMedications().then((medications: any) => {
        this.medications = medications;
      });
      // Get the assigned team members for this care plan
      let teamMembersSub = this.store.CarePlan.detailRoute('get', this.plan.id, 'care_team_members').subscribe(
        (teamMembers: any) => {
          this.careTeamMembers = teamMembers;
        },
        (err) => {},
        () => {
          teamMembersSub.unsubscribe();
        }
      );
    }
  }

  public fetchMedications() {
    let promise = new Promise((resolve, reject) => {
      let medicationsSub = this.store.Medication.readListPaged({}).subscribe(
        (medications) => resolve(medications),
        (err) => reject(err),
        () => medicationsSub.unsubscribe()
      )
    });
    return promise;
  }

  public saveDisabled() {
    return (
      !this.plan || !this.selectedMedication || !this.doseMg ||
      !this.datePrescribed || !this.durationDays || !this.startDay ||
      !this.frequency || !this.repeatAmount || !this.appearTime || !this.dueTime
    );
  }

  public clickCancel() {
    this.modal.close(null);
  }

  public clickSave() {
    let returnData = {
      patient_medication: {
        patient: this.plan.patient,
        medication: this.selectedMedication,
        dose_mg: this.doseMg,
        date_prescribed: this.datePrescribed.format('YYYY-MM-DD'),
        duration_days: this.durationDays,
        prescribing_practitioner: this.prescribingPractitioner,
      },
      task: {
        start_on_day: this.startDay,
        frequency: this.frequency,
        repeat_amount: this.repeatsChoice === 'plan_end' ? -1 : this.repeatAmount,
        appear_time: this.appearTime,
        due_time: this.dueTime,
        plan: this.plan.id,
      }
    };
    this.modal.close(returnData);
  }
}
