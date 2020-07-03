import { IDiagnosis } from './diagnosis';
import { IEmployee } from './employee';
import { ISearchablePatient } from './searchable-patient';

export interface IFilteredResults {
  billingPractioner?: {
    array: Array<IEmployee>,
    search: string
  },
  careManager?: {
    array: Array<IEmployee>,
    search: string
  },
  diagnosis?: {
    array: Array<IDiagnosis>,
    search: string
  },
  patients?: {
    array: Array<ISearchablePatient>,
    search: string
  },
}
