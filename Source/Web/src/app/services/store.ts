import { Observable } from 'rxjs/Observable';
import 'rxjs/add/observable/combineLatest';
import 'rxjs/add/observable/of';
import 'rxjs/add/observable/throw';
import 'rxjs/add/operator/catch';
import 'rxjs/add/operator/map';
import 'rxjs/add/operator/mergeMap';
import { AppConfig } from '../app.config';
import { HttpService } from './http.service';
import { throwError, of, combineLatest } from 'rxjs';

interface ListResponse {
  results: any[];
  count: number;
  previous: string;
  next: string;
}

export class Store {

  private http: HttpService;
  private endpoint: string;

  constructor(http: HttpService, endpoint: string) {
    this.http = http;
    this.endpoint = endpoint;
  }

  public create(payload: any): Observable<any> {
    let request = this.http.post(this.createUrl(), payload);
    return request.catch((error: any) => {
      return throwError(error);
    });
  }

  public createAlt(payload: any): Observable<any> {
    let request = this.http.post(this.createRestAuthUrl(), payload);
    return request.catch((error: any) => {
      return throwError(error);
    });
  }

  public read(id: number | string): Observable<any> {
    let request = this.http.get(this.createUrl(id));
    return request;
  }

  public readList(params = {}): Observable<any> {
    let request = this.http.get(this.createUrl(), params);
    return request
      .map((response: ListResponse) => {
        const results = Object.assign(response.results, {
          count: response.count,
          next: response.next,
          previous: response.previous
        });
        return response;
      }).catch((error: any) => {
        return throwError(error);
      });
  }

  public readListPaged(params = {}): Observable<any> {
    let request = this.http.get(this.createUrl(), params);
    return request
      .flatMap((firstPage: ListResponse) => {
        let pageObservables: Observable<any>[] = [ of(firstPage.results)];
        // construct each page url for each existing page, starting at 2
        if (firstPage.next) {
          for (let i = 2; i <= Math.ceil(firstPage.count / firstPage.results.length); i++) {
            const page = this.http.get(this.createUrl(), Object.assign(params, { page: i }))
              .map((pageResponse: ListResponse) => pageResponse.results);
            pageObservables.push(page);
          }
        }
        return combineLatest(pageObservables)
          .map((nested) => nested.reduce((acc, cur) => acc.concat(cur), [])).catch((error: any) => {
            return throwError(error);
          });
      }).catch((error: any) => {
        return throwError(error);
      });
  }

  public update(id: number | string, payload: any, patch = true): Observable<any> {
    let request = null;
    if (patch) {
      request = this.http.patch(this.createUrl(id), payload);
    } else {
      request = this.http.put(this.createUrl(id), payload);
    }
    return request.catch((error: any) => {
      return throwError(error);
    });
  }

  public updateAlt(id: number | string, payload: any, patch = true): Observable<any> {
    let request = null;
    if (patch) {
      request = this.http.patch(this.createRestAuthUrl(id), payload);
    } else {
      request = this.http.put(this.createRestAuthUrl(id), payload);
    }
    return request.catch((error: any) => {
      return throwError(error);
    });
  }

  public destroy(id: number | string): Observable<any> {
    let request = this.http.delete(this.createUrl(id));
    return request.catch((error: any) => {
      return throwError(error);
    });
  }

  public detailRoute(method: string, id: number | string, route: string, payload = {}, params = {}) {
    let request = this.http.request(method, `${this.createUrl(id)}${route}/`, payload, params);
    return request.catch((error: any) => {
      return throwError(error);
    });
  }

  public listRoute(method: string, route: string, payload = {}, params = {}) {
    let request = this.http.request(method, `${this.createUrl()}${route}/`, payload, params);
    return request.catch((error: any) => {
      return throwError(error);
    });
  }

  private createUrl(id: number | string = null): string {
    if (id) {
      return `${AppConfig.apiUrl}${this.endpoint}/${id}/`;
    } else {
      return `${AppConfig.apiUrl}${this.endpoint}/`;
    }
  }

  private createRestAuthUrl(id: number | string = null):string {
    if (id) {
      return `${AppConfig.restAuthUrl}${this.endpoint}/${id}/`;
    } else {
      return `${AppConfig.restAuthUrl}${this.endpoint}/`;
    }
  }
}
