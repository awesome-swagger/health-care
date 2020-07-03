
export interface IApiResultsContainer < T > {
  count?: number;
  next?: any;
  previous?: any;
  results?: T;
}
