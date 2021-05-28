using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Backend.Loggers
{
    public class ConsoleLogger : ILogger
    {
        public void LogError(string message)
        {
            Console.WriteLine(String.Format("Error: {0}", message));
        }

        public void LogError(Exception ex)
        {
            Console.WriteLine(String.Format("Error: {0}", ex.Message));
        }
    }
}
