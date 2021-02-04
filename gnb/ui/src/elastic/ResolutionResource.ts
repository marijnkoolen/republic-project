import {Client} from "elasticsearch";
import AggsQuery from "./model/AggsQuery";
import FilterRange from "./model/FilterRange";
import AggsResolutionHistogram from "./model/AggsResolutionHistogram";
import {PersonType} from "./model/PersonType";
import FilterFullText from "./model/FilterFullText";
import FilterPeople from "./model/FilterPeople";
import Resolution from "./model/Resolution";

import {
  ERR_ES_AGGREGATE_RESOLUTIONS,
  ERR_ES_AGGREGATE_RESOLUTIONS_BY_PERSON,
  ERR_ES_GET_MULTI_RESOLUTIONS
} from "../Placeholder";
import {handleEsError} from "./EsErrorHandler";
import AggWithIdFilter from "./model/AggWithIdFilter";
import AggWithFilters from "./model/AggWithFilters";

/**
 * ElasticSearch Resolution Resource
 */
export default class ResolutionResource {

  private esClient: Client;
  private index: string;

  constructor(esClient: Client) {
    this.esClient = esClient;
    this.index = 'gnb-resolutions';
  }

  /**
   * Aggregate resolutions:
   * - by attendant
   * - by mentioned
   * - between start and end date (up to and including)
   */
  public async aggregateBy(
    attendants: number[],
    mentioned: number[],
    begin: Date,
    end: Date,
    fullText: string
  ): Promise<any> {
    const query = new AggWithFilters();

    query.addFilter(new FilterRange(begin, end));

    if (fullText) {
      query.addFilter(new FilterFullText(fullText));
    }

    for (const a of attendants) {
      query.addFilter(new FilterPeople(a, PersonType.ATTENDANT));
    }

    for (const m of mentioned) {
      query.addFilter(new FilterPeople(m, PersonType.MENTIONED));
    }

    const hist = new AggsResolutionHistogram(begin, end, 1);
    query.addAgg(hist);

    const response = await this.esClient
      .search(new AggsQuery(query))
      .catch(e => handleEsError(e, ERR_ES_AGGREGATE_RESOLUTIONS));

    return response.aggregations
      .filtered_aggs
      .resolution_histogram
      .buckets;
  }

  /**
   * Get multiple resolutions from gnb-resolutions
   */
  public async getMulti(
    ids: string[]
  ): Promise<Resolution[]> {
    if (ids.length === 0) {
      return [];
    }
    const params = {index: this.index, body: {ids}};
    const response = await this.esClient
      .mget<Resolution>(params)
      .catch(e => handleEsError(e, ERR_ES_GET_MULTI_RESOLUTIONS));

    if (response.docs) {
      return response.docs.map(d => d._source) as Resolution[];
    } else {
      return [];
    }
  }

  /**
   * TODO: cleanup
   * @param resolutions
   * @param id
   * @param type
   * @param begin
   * @param end
   */
  public async aggregateByPerson(
    resolutions: string[],
    id: number,
    type: PersonType,
    begin: Date,
    end: Date
  ): Promise<Resolution[]> {

    if (resolutions.length === 0) {
      return [];
    }

    const filteredQuery = new AggWithFilters();
    filteredQuery.addFilter(new FilterPeople(id, type));

    const sortedResolutions = resolutions.sort();
    filteredQuery.addAgg(new AggsResolutionHistogram(begin, end, 1));

    const aggWithIdFilter = new AggWithIdFilter(sortedResolutions);
    aggWithIdFilter.addAgg(filteredQuery);

    const aggsQuery = new AggsQuery(aggWithIdFilter);

    const response = await this.esClient
      .search(aggsQuery)
      .catch(e => handleEsError(e, ERR_ES_AGGREGATE_RESOLUTIONS_BY_PERSON));

    return response.aggregations
      .id_filtered_aggs
      .filtered_aggs
      .resolution_histogram
      .buckets;

  }
}
