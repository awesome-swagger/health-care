import { Component, OnDestroy, OnInit } from '@angular/core';
import * as moment from 'moment';
import { sumBy as _sumBy, uniqBy as _uniqBy, groupBy as _groupBy } from 'lodash';
import { StoreService } from '../../services';
import mockData from './billingData';

@Component({
  selector: 'app-billing',
  templateUrl: './billing.component.html',
  styleUrls: ['./billing.component.scss'],
})
export class BillingComponent implements OnDestroy, OnInit {

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
  public selectedStatus = '';
  public employees = [];
  public employeeSearch = '';
  public planTypes = [];

  constructor(
    private store: StoreService,
  ) { }

  public syncTooltipOpen = false;
  public filterFacilitiesOpen = false;
  public filterServiceOpen = false;
  public filterStatusOpen = false;
  public employeeSearchOpen = false;
  public billablePatientsHelpOpen = false;
  public practitionerDropdownOpen = {};
  public detailsOpen = {};

  public ngOnInit() {
    this.patients = mockData.patients;
    this.billingData = mockData.billingData;
    console.log(this.billingData);
    this.facilities = this.getUniqueFacilities();
    this.facilitiesShown = this.facilities.concat();
    this.selectedFacilities = this.facilities.concat();
    this.serviceAreas = this.getUniqueServiceAreas();
    this.serviceAreasShown = this.serviceAreas.concat();
    this.selectedServiceAreas = this.serviceAreas.concat();
    this.employees = this.getUniqueBPs();
    this.planTypes = mockData.billingTypes;
  }

  public ngOnDestroy() { }

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
    console.log(this.selectedFacilities);
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

  public toggleServiceArea(serviceArea) {
    if (this.isServiceAreaSelected(serviceArea)) {
      let index = this.selectedServiceAreas.findIndex((obj) => obj.id === serviceArea.id);
      this.selectedServiceAreas.splice(index, 1);
    } else {
      this.selectedServiceAreas.push(serviceArea);
    }
    console.log(this.selectedServiceAreas);
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
    return Object.keys(_groupBy(this.billingData, (obj) => obj.patient)).length;
  }

  public totalFacilities() {
    return Object.keys(_groupBy(this.billingData, (obj) => {
      return this.getPatient(obj.patient).facility;
    })).length;
  }

  public totalPractitioners() {
    return Object.keys(_groupBy(this.billingData, (obj) => obj.billingPractitioner)).length;
  }

  public totalHours() {
    return this.minutesToHours(_sumBy(this.billingData, (obj) => {
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
    return _sumBy(this.billingData, (obj) => {
      return _sumBy(obj.entries, (objEntry) => {
        return objEntry.subtotal;
      });
    });
  }

  public getAllBPsForFacility(facility) {
    return this.billingData.filter((obj) => this.getPatient(obj.patient).facility === facility).map(
      (obj) => this.getEmployee(obj.billingPractitioner));
  }

  public billingDataByBP(bp, facility) {
    return this.billingData.filter((obj) => obj.billingPractitioner === bp && this.getPatient(obj.patient).facility === facility);
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
