import { async, ComponentFixture, TestBed } from '@angular/core/testing';
import { AppModule } from '../../../app.module';
import { PlanInfoComponent } from './info.component';

describe('PlanInfoComponent', () => {
  let component: PlanInfoComponent;
  let fixture: ComponentFixture<PlanInfoComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      imports: [
        AppModule
      ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(PlanInfoComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should be created', () => {
    expect(component).toBeTruthy();
  });
});
