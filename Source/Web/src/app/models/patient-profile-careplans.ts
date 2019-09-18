import { ICarePlan } from './care-plan';

export interface IPatientProfileCarePlans
{
  id: string;
  plan_template: ICarePlan;
  goals: Array<{}>;
};
