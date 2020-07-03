import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { AddCtComponent } from './add-ct.component';

describe('AddCtComponent', () => {
  let component: AddCtComponent;
  let fixture: ComponentFixture<AddCtComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ AddCtComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(AddCtComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
