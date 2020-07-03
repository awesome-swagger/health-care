import { Component, OnInit } from '@angular/core';
import { StoreService, AuthService } from '../../../../../services';
import { ModalService } from '../../../../../modules/modals';

@Component({
  selector: 'app-add-user-to-facility',
  templateUrl: './add-user-to-facility.component.html',
  styleUrls: ['./add-user-to-facility.component.scss']
})
export class AddUserToFacilityComponent implements OnInit {

  public facilities = [];
  public selectedFacility = null;

  constructor(
    private auth: AuthService,
    private modals: ModalService,
    private store: StoreService,
  ) { }

  ngOnInit() {

    this.auth.organization$.subscribe(org => {
      if (!org) return;
      
      this.store.Organization.detailRoute('GET', org.id, 'facilities').subscribe((res:any) => {
        this.facilities = res.results.filter(f => !f.is_affiliate);
      })

    })
  }

  close() {
    this.modals.close(null);
  }

  public get submitDisabled() {
    return !this.selectedFacility;
  }

  submit() {
    this.modals.close(this.selectedFacility)
  }

}
