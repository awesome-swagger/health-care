import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { AddUserToFacilityComponent } from './add-user-to-facility.component';

describe('AddUserToFacilityComponent', () => {
  let component: AddUserToFacilityComponent;
  let fixture: ComponentFixture<AddUserToFacilityComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ AddUserToFacilityComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(AddUserToFacilityComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
