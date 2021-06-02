using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Backend.Loggers
{
    public interface ILogger
    {
        void LogError(string message);
        void LogError(Exception ex);
    }
}
