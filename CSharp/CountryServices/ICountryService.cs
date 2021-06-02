using Backend.Models;
using System.Collections.Generic;
using System.Threading.Tasks;

namespace Backend.CountryServices
{
    public interface ICountryService
    {
        Task<List<Country>> GetCountries();
    }
}