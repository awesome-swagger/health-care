import { Component, OnDestroy, OnInit } from '@angular/core';
import  { Subscription } from 'rxjs';
import * as moment from 'moment';
import { sumBy as _sumBy, uniqBy as _uniqBy, groupBy as _groupBy } from 'lodash';
import { AuthService, StoreService } from '../../services';
import mockData from './billingData';

@Component({
  selector: 'app-billing',
  templateUrl: './billing.component.html',
  styleUrls: ['./billing.component.scss'],
})
export class BillingComponent implements OnDestroy, OnInit {

  public user = null;
  public organization = null;
  public isManager = false;
  public selectedMonth: moment.Moment = moment().startOf('month');
  public billingData = null;
  public patients = [];
  public facilities = [];
  public facilitiesShown = [];
  public selectedFacilities = [];
  public facilitySearch = '';
  public serviceAreas = [];
  public serviceAreasShown = [];
  public selectedServiceAreas = [];
  public serviceSearch = '';
  public selectedStatus = 'all';
  public employees = [];
  public employeesShown = [];
  public employeeSearch = '';
  public selectedEmployee = null;
  public planTypes = [];

  public syncTooltipOpen = false;
  public filterFacilitiesOpen = false;
  public filterServiceOpen = false;
  public filterStatusOpen = false;
  public employeeSearchOpen = false;
  public billablePatientsHelpOpen = false;
  public practitionerDropdownOpen = {};
  public detailsOpen = {};

  private authSub: Subscription = null;
  private orgSub: Subscription = null;

  constructor(
    private auth: AuthService,
    private store: StoreService,
  ) { }

  public ngOnInit() {
    this.patients = mockData.patients;
    this.billingData = mockData.billingData;
    this.facilities = this.getUniqueFacilities();
    this.facilitiesShown = this.facilities.concat();
    this.selectedFacilities = this.facilities.concat();
    this.serviceAreas = this.getUniqueServiceAreas();
    this.serviceAreasShown = this.serviceAreas.concat();
    this.selectedServiceAreas = this.serviceAreas.concat();
    this.employees = this.getUniqueBPs();
    this.planTypes = mockData.billingTypes;
    this.authSub = this.auth.user$.subscribe((user) => {
      if (!user) {
        return;
      }
      this.auth.organization$.subscribe((organization) => {
        this.user = user;
      });
    });
    this.orgSub = this.auth.organization$.subscribe((organization) => {
      if (!organization) {
        return;
      }
      this.organization = organization;
      this.isManager = this.organization.is_manager;
    });
  }

  public ngOnDestroy() {
    if (this.authSub) {
      this.authSub.unsubscribe();
    }
  }

  public filteredBilling() {
    return this.billingData.filter((billingObj) => {
      if (this.selectedStatus === 'all') {
        return true;
      } else if (this.selectedStatus === 'not-billed') {
        return !billingObj.isBilled;
      } else if (this.selectedStatus === 'billed') {
        return billingObj.isBilled;
      } else {
        return true;
      }
    }).filter((billingObj) => {
      let facilityValues = this.selectedFacilities.map((obj) => obj.id);
      let serviceAreaValues = this.selectedServiceAreas.map((obj) => obj.id);
      return (
        facilityValues.includes(this.getPatient(billingObj.patient).facility) &&
        serviceAreaValues.includes(billingObj.serviceArea)
      );
    }).filter((billingObj) => {
      if (!this.selectedEmployee) {
        return true;
      }
      return billingObj.billingPractitioner === this.selectedEmployee.id;
    });
  }

  public getPillColor(percentage) {
    if (percentage >= 90) {
      return '#4caf50';
    } else if (percentage <= 89 && percentage >= 70) {
      return '#ff9800';
    } else if (percentage <= 69 && percentage >= 50) {
       return '#ca2c4e';
    } else {
      return '#880e4f';
    }
  }

  public getUniqueFacilities() {
    return _uniqBy(this.billingData.map((obj) => this.getFacility(this.getPatient(obj.patient).facility)), (obj) => obj.id);
  }

  public getUniqueServiceAreas() {
    return _uniqBy(this.billingData.map((obj) => this.getServiceArea(obj.serviceArea)), (obj) => obj.id);
  }

  public getUniqueBPs() {
    return _uniqBy(this.billingData.map((obj) => this.getEmployee(obj.billingPractitioner)), (obj) => obj.id);
  }

  public decrementMonth() {
    this.selectedMonth.add(-1, 'month');
  }

  public incrementMonth() {
    this.selectedMonth.add(1, 'month');
  }

  public isFacilitySelected(facility) {
    return this.selectedFacilities.findIndex((obj) => obj.id === facility.id) !== -1;
  }

  public checkAllFacilities() {
    this.selectedFacilities = mockData.facilities.concat();
  }

  public uncheckAllFacilities() {
    this.selectedFacilities = [];
  }

  public filterFacilities() {
    this.facilitiesShown = this.facilities.filter((obj) => {
      return obj.name.toLowerCase().includes(this.facilitySearch.toLowerCase());
    });
  }

  public toggleFacility(facility) {
    if (this.isFacilitySelected(facility)) {
      let index = this.selectedFacilities.findIndex((obj) => obj.id === facility.id);
      this.selectedFacilities.splice(index, 1);
    } else {
      this.selectedFacilities.push(facility);
    }
  }

  public isServiceAreaSelected(serviceArea) {
    return this.selectedServiceAreas.findIndex((obj) => obj.id === serviceArea.id) !== -1;
  }

  public checkAllServiceAreas() {
    this.selectedServiceAreas = this.serviceAreas.concat();
  }

  public uncheckAllServiceAreas() {
    this.selectedServiceAreas = [];
  }

  public filterServiceArea() {
    this.serviceAreasShown = this.serviceAreas.filter((obj) => {
      return obj.name.toLowerCase().includes(this.serviceSearch.toLowerCase());
    });
  }

  public filterEmployee() {
    this.employeesShown = this.employees.filter((obj) => {
      let fullNameWithTitle = `${obj.first_name} ${obj.last_name}, ${obj.title}`;
      return fullNameWithTitle.toLowerCase().includes(this.employeeSearch.toLowerCase());
    });
  }

  public setSelectedEmployee(employee) {
    this.selectedEmployee = employee;
    this.employeeSearch = `${employee.first_name} ${employee.last_name}, ${employee.title}`;
  }

  public toggleServiceArea(serviceArea) {
    if (this.isServiceAreaSelected(serviceArea)) {
      let index = this.selectedServiceAreas.findIndex((obj) => obj.id === serviceArea.id);
      this.selectedServiceAreas.splice(index, 1);
    } else {
      this.selectedServiceAreas.push(serviceArea);
    }
  }

  public getPatient(id) {
    return mockData.patients.find((obj) => obj.id === id);
  }

  public getFacility(id) {
    return mockData.facilities.find((obj) => obj.id === id);
  }

  public getServiceArea(id) {
    return mockData.serviceAreas.find((obj) => obj.id === id);
  }

  public getEmployee(id) {
    return mockData.employees.find((obj) => obj.id === id);
  }

  public getBillingType(id) {
    return mockData.billingTypes.find((obj) => obj.id === id);
  }

  public totalBillablePatients() {
    return Object.keys(_groupBy(this.filteredBilling(), (obj) => obj.patient)).length;
  }

  public totalFacilities() {
    return Object.keys(_groupBy(this.filteredBilling(), (obj) => {
      return this.getPatient(obj.patient).facility;
    })).length;
  }

  public totalPractitioners() {
    return Object.keys(_groupBy(this.filteredBilling(), (obj) => obj.billingPractitioner)).length;
  }

  public totalHours() {
    return this.minutesToHours(_sumBy(this.filteredBilling(), (obj) => {
      return _sumBy(obj.entries, (objEntry) => {
        return objEntry.totalMinutes;
      });
    }));
  }

  public minutesToHours(n) {
    let num = n;
    let hours = (num / 60);
    let rhours = Math.floor(hours);
    let minutes = (hours - rhours) * 60;
    let rminutes = Math.round(minutes);
    return `${rhours}:${rminutes}`;
  }

  public totalDollars() {
    return _sumBy(this.filteredBilling(), (obj) => {
      return _sumBy(obj.entries, (objEntry) => {
        return objEntry.subtotal;
      });
    });
  }

  public facilityBillablePatients(facility) {
    return _uniqBy(
        this.filteredBilling()
        .filter(
          (obj) => this.getPatient(obj.patient).facility === facility)
        .map(
          (obj) => this.getPatient(obj.patient)),
        (obj) => obj.id).length;
  }

  public getAllBPsForFacility(facility) {
    return this.filteredBilling().filter((obj) => this.getPatient(obj.patient).facility === facility).map(
      (obj) => this.getEmployee(obj.billingPractitioner));
  }

  public billingDataByBP(bp, facility) {
    return this.filteredBilling().filter((obj) => obj.billingPractitioner === bp && this.getPatient(obj.patient).facility === facility);
  }

  public bpBillablePatients(bp, facility) {
    return Object.keys(_groupBy(this.billingDataByBP(bp, facility), (obj) => obj.patient)).length;
  }

  public patientsBilled(billingData) {
    return billingData.filter((obj) => obj.isBilled).length;
  }

  public percentBilled(bp, facility) {
    return (this.patientsBilled(this.billingDataByBP(bp, facility)) / this.bpBillablePatients(bp.id, facility.id))
  }

  public entriesSubtotal(entries) {
    return _sumBy(entries, (obj) => obj.subtotal);
  }
}
